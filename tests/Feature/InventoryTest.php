<?php

namespace Tests\Feature;

use App\Models\Category;
use App\Models\Movement;
use App\Models\Product;
use App\Models\User;
use App\Services\InventoryService;
use Illuminate\Database\QueryException;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\DB;
use Illuminate\Validation\ValidationException;
use PHPUnit\Framework\Attributes\DataProvider;
use Tests\TestCase;

class InventoryTest extends TestCase
{
    use RefreshDatabase;

    private User $admin;

    private Product $product;

    protected function setUp(): void
    {
        parent::setUp();
        $this->admin = User::factory()->create();
        $category = Category::create(['name' => 'Bebidas']);
        $this->product = app(InventoryService::class)->createProduct(['name' => 'Agua mineral', 'sku' => 'BEB-001', 'category_id' => $category->id, 'price' => 3.50, 'minimum_stock' => 3, 'initial_stock' => 10], $this->admin);
        $this->actingAs($this->admin);
    }

    private function data(array $overrides = []): array
    {
        return array_replace(['product_id' => $this->product->id, 'type' => 'entrada', 'quantity' => 5, 'note' => 'Reposición'], $overrides);
    }

    public function test_entry_increases_stock_and_records_history(): void
    {
        $this->post(route('movements.store'), $this->data())->assertRedirect(route('movements.index'))->assertSessionHasNoErrors();
        $this->assertSame(15, $this->product->refresh()->stock);
        $this->assertDatabaseHas('movements', ['product_id' => $this->product->id, 'quantity' => 5, 'previous_stock' => 10, 'resulting_stock' => 15, 'type' => 'entrada', 'user_id' => $this->admin->id]);
        $this->get(route('movements.index'))->assertOk()->assertSee('Reposición')->assertSee($this->admin->name);
    }

    public function test_exit_decreases_stock_and_alert_appears_at_exact_minimum(): void
    {
        $this->post(route('movements.store'), $this->data(['type' => 'salida', 'quantity' => 7]))->assertSessionHasNoErrors();
        $this->assertSame(3, $this->product->refresh()->stock);
        $this->assertDatabaseHas('movements', ['type' => 'salida', 'previous_stock' => 10, 'resulting_stock' => 3]);
        $this->get(route('products.low-stock'))->assertOk()->assertSee('Agua mineral')->assertSee('Stock bajo');
        $this->get(route('dashboard'))->assertViewHas('lowStockCount', 1)->assertViewHas('totalUnits', 3);
    }

    public function test_exact_stock_exit_is_allowed_and_marks_product_out_of_stock(): void
    {
        $this->post(route('movements.store'), $this->data(['type' => 'salida', 'quantity' => 10]))->assertSessionHasNoErrors();
        $this->assertSame(0, $this->product->refresh()->stock);
        $this->get(route('products.low-stock'))->assertSee('Agotado');
        $this->get(route('dashboard'))->assertViewHas('outOfStockCount', 1);
    }

    public function test_insufficient_stock_preserves_balance_and_history(): void
    {
        $this->post(route('movements.store'), $this->data(['type' => 'salida', 'quantity' => 11]))->assertSessionHasErrors('quantity');
        $this->assertSame(10, $this->product->refresh()->stock);
        $this->assertDatabaseCount('movements', 1);
    }

    #[DataProvider('invalidMovements')]
    public function test_invalid_movement_is_rejected(string $field, mixed $value): void
    {
        $response = $this->post(route('movements.store'), $this->data([$field => $value]));
        $response->assertSessionHasErrors($field);
        if ($field === 'quantity' && in_array($value, [0, -1], true)) {
            $response->assertSessionHasErrors(['quantity' => 'La cantidad debe ser mayor o igual a 1.']);
        }
        if ($field === 'quantity' && $value === Product::MAX_STOCK + 1) {
            $response->assertSessionHasErrors(['quantity' => 'La cantidad no debe superar 2147483647.']);
        }
        $this->assertSame(10, $this->product->refresh()->stock);
        $this->assertDatabaseCount('movements', 1);
    }

    public static function invalidMovements(): array
    {
        return [['quantity', 0], ['quantity', -1], ['quantity', 1.5], ['quantity', 'abc'], ['quantity', null], ['product_id', 999], ['type', 'ajuste'], ['quantity', Product::MAX_STOCK + 1]];
    }

    public function test_inactive_product_rejects_movements_in_request_and_service(): void
    {
        $this->product->update(['is_active' => false]);
        $this->post(route('movements.store'), $this->data())->assertSessionHasErrors('product_id');
        try {
            app(InventoryService::class)->record($this->product, 'entrada', 2, $this->admin);
            $this->fail('Inactive product accepted a movement.');
        } catch (ValidationException $exception) {
            $this->assertArrayHasKey('product_id', $exception->errors());
        }
        $this->assertSame(10, $this->product->refresh()->stock);
        $this->get(route('dashboard'))->assertViewHas('totalProducts', 0)->assertViewHas('totalUnits', 0);
    }

    public function test_service_uses_current_database_balance_instead_of_stale_model(): void
    {
        $service = app(InventoryService::class);
        $service->record($this->product, 'salida', 7, $this->admin);
        $service->record($this->product, 'entrada', 2, $this->admin);
        $this->assertSame(5, $this->product->refresh()->stock);
        $this->assertDatabaseHas('movements', ['previous_stock' => 3, 'resulting_stock' => 5]);
    }

    public function test_movement_failure_rolls_back_stock_update(): void
    {
        $unknownUser = new User;
        $unknownUser->id = 999;
        try {
            app(InventoryService::class)->record($this->product, 'entrada', 5, $unknownUser);
            $this->fail('Invalid foreign key was accepted.');
        } catch (QueryException) {
            $this->assertSame(10, $this->product->refresh()->stock);
            $this->assertDatabaseCount('movements', 1);
        }
    }

    public function test_database_rejects_negative_stock(): void
    {
        $this->expectException(QueryException::class);
        DB::table('products')->where('id', $this->product->id)->update(['stock' => -1]);
    }

    public function test_history_filters_and_pagination_preserve_filter(): void
    {
        for ($i = 0; $i < 12; $i++) {
            app(InventoryService::class)->record($this->product, 'entrada', 1, $this->admin, 'Entrada '.$i);
        }
        $response = $this->get(route('movements.index', ['type' => 'entrada', 'product_id' => $this->product->id]));
        $response->assertOk()->assertViewHas('movements', fn ($movements) => $movements->total() === 13 && $movements->count() === 10)->assertSee('Siguiente');
        $this->get(route('movements.index', ['type' => 'salida']))->assertSee('No hay movimientos para mostrar');
    }

    public function test_replenishment_removes_alert_and_inactive_products_are_excluded(): void
    {
        app(InventoryService::class)->record($this->product, 'salida', 8, $this->admin);
        $this->get(route('products.low-stock'))->assertSee('Agua mineral');
        app(InventoryService::class)->record($this->product, 'entrada', 5, $this->admin);
        $this->get(route('products.low-stock'))->assertDontSee('Agua mineral')->assertSee('Sin alertas pendientes');
    }

    public function test_history_has_no_edit_or_delete_endpoints(): void
    {
        $movement = Movement::first();
        $this->put('/movements/'.$movement->id, ['quantity' => 100])->assertStatus(404);
        $this->delete('/movements/'.$movement->id)->assertStatus(404);
        $this->assertDatabaseCount('movements', 1);
    }
}
