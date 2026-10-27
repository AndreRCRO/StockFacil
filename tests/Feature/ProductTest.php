<?php

namespace Tests\Feature;

use App\Models\Category;
use App\Models\User;
use App\Services\InventoryService;
use Illuminate\Database\QueryException;
use Illuminate\Foundation\Testing\RefreshDatabase;
use PHPUnit\Framework\Attributes\DataProvider;
use Tests\TestCase;

class ProductTest extends TestCase
{
    use RefreshDatabase;

    private User $admin;

    private Category $category;

    protected function setUp(): void
    {
        parent::setUp();
        $this->admin = User::factory()->create();
        $this->category = Category::create(['name' => 'Bebidas']);
        $this->actingAs($this->admin);
    }

    private function data(array $overrides = []): array
    {
        return array_replace(['name' => 'Agua mineral', 'sku' => 'BEB-001', 'category_id' => $this->category->id, 'price' => '3.50', 'initial_stock' => 10, 'minimum_stock' => 3], $overrides);
    }

    public function test_valid_product_appears_in_listing_with_traceable_initial_stock(): void
    {
        $this->post(route('products.store'), $this->data(['sku' => ' beb-001 ']))->assertRedirect(route('products.index'))->assertSessionHasNoErrors();
        $this->assertDatabaseHas('products', ['sku' => 'BEB-001', 'stock' => 10, 'price' => 3.50]);
        $this->assertDatabaseHas('movements', ['type' => 'entrada', 'quantity' => 10, 'previous_stock' => 0, 'resulting_stock' => 10, 'user_id' => $this->admin->id, 'note' => 'Stock inicial']);
        $this->get(route('products.index'))->assertOk()->assertSee('Agua mineral')->assertSee('BEB-001');
    }

    #[DataProvider('invalidProducts')]
    public function test_invalid_product_is_rejected(string $field, mixed $value): void
    {
        $this->followingRedirects()->from(route('products.create'))->post(route('products.store'), $this->data([$field => $value]))->assertOk()->assertSee('Revisa los datos antes de guardar.');
        $this->assertDatabaseCount('products', 0);
        $this->assertDatabaseCount('movements', 0);
    }

    public static function invalidProducts(): array
    {
        return [['name', ''], ['sku', ''], ['sku', ['invalid']], ['price', -1], ['price', 'abc'], ['price', '3.501'], ['initial_stock', -1], ['initial_stock', 1.5], ['minimum_stock', -1], ['category_id', 999], ['stock', 500]];
    }

    public function test_duplicate_sku_is_rejected_even_with_lowercase(): void
    {
        $this->post(route('products.store'), $this->data());
        $this->post(route('products.store'), $this->data(['sku' => 'beb-001']))->assertSessionHasErrors('sku');
        $this->assertDatabaseCount('products', 1);
    }

    public function test_zero_initial_stock_and_zero_price_are_valid_without_zero_movement(): void
    {
        $this->post(route('products.store'), $this->data(['price' => 0, 'initial_stock' => 0]))->assertSessionHasNoErrors();
        $this->assertDatabaseHas('products', ['stock' => 0, 'price' => 0]);
        $this->assertDatabaseCount('movements', 0);
    }

    public function test_initial_movement_failure_rolls_back_product_creation(): void
    {
        $unknownUser = new User;
        $unknownUser->id = 999;
        try {
            app(InventoryService::class)->createProduct($this->data(), $unknownUser);
            $this->fail('An invalid initial movement was accepted.');
        } catch (QueryException) {
            $this->assertDatabaseCount('products', 0);
            $this->assertDatabaseCount('movements', 0);
        }
    }

    public function test_edit_updates_information_but_cannot_modify_stock(): void
    {
        $product = app(InventoryService::class)->createProduct($this->data(), $this->admin);
        $edit = $this->data(['name' => 'Agua actualizada']);
        unset($edit['initial_stock']);
        $this->put(route('products.update', $product), $edit)->assertSessionHasNoErrors();
        $this->assertSame('Agua actualizada', $product->refresh()->name);
        $this->assertSame(10, $product->stock);
        $this->put(route('products.update', $product), $edit + ['stock' => 999])->assertSessionHasErrors('stock');
        $this->put(route('products.update', $product), $edit + ['initial_stock' => 999])->assertSessionHasErrors('initial_stock');
        $this->assertSame(10, $product->refresh()->stock);
        $this->assertDatabaseCount('movements', 1);
    }

    public function test_deactivation_preserves_history_and_hides_from_active_listing(): void
    {
        $product = app(InventoryService::class)->createProduct($this->data(), $this->admin);
        $this->patch(route('products.deactivate', $product))->assertRedirect(route('products.index'));
        $this->assertFalse($product->refresh()->is_active);
        $this->assertDatabaseCount('movements', 1);
        $this->get(route('products.index'))->assertDontSee('Agua mineral');
        $this->get(route('products.index', ['status' => 'inactive']))->assertSee('Agua mineral')->assertSee('Inactivo');
        $this->get(route('movements.index'))->assertSee('Agua mineral');
    }

    public function test_search_and_category_filter_work_together(): void
    {
        $other = Category::create(['name' => 'Snacks']);
        app(InventoryService::class)->createProduct($this->data(), $this->admin);
        app(InventoryService::class)->createProduct($this->data(['name' => 'Galletas', 'sku' => 'SNK-001', 'category_id' => $other->id]), $this->admin);
        $this->get(route('products.index', ['q' => 'BEB-001', 'category_id' => $this->category->id]))->assertSee('Agua mineral')->assertDontSee('Galletas');
        $this->get(route('products.index', ['q' => 'BEB-001', 'category_id' => $other->id]))->assertSee('No encontramos productos')->assertDontSee('Agua mineral');
    }
}
