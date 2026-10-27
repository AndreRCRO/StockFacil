<?php

namespace Tests\Feature;

use App\Models\Product;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Hash;
use Tests\TestCase;

class SeederTest extends TestCase
{
    use RefreshDatabase;

    public function test_seed_is_repeatable_and_demo_history_matches_balances(): void
    {
        $this->seed();
        $this->seed();
        $this->assertDatabaseCount('products', 12);
        $this->assertDatabaseCount('categories', 5);
        $this->assertDatabaseCount('movements', 24);
        $this->assertDatabaseCount('users', 1);
        $admin = User::first();
        $this->assertTrue(Hash::check(config('stockfacil.admin_password'), $admin->password));
        foreach (Product::with('movements')->get() as $product) {
            $balance = 0;
            foreach ($product->movements->sortBy('id') as $movement) {
                $this->assertSame($balance, $movement->previous_stock);
                $balance += $movement->type === 'entrada' ? $movement->quantity : -$movement->quantity;
                $this->assertSame($balance, $movement->resulting_stock);
            }
            $this->assertSame($balance, $product->stock);
        }
        $this->actingAs($admin)->get(route('dashboard'))->assertOk()->assertViewHas('totalProducts', 12)->assertViewHas('totalUnits', 184)->assertViewHas('lowStockCount', 5)->assertViewHas('outOfStockCount', 2);
        $this->get(route('products.index'))->assertViewHas('products', fn ($products) => $products->total() === 12 && $products->count() === 10);
    }
}
