<?php

namespace Database\Seeders;

use App\Models\Category;
use App\Models\Movement;
use App\Models\Product;
use App\Models\User;
use App\Services\InventoryService;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class DemoInventorySeeder extends Seeder
{
    public function run(): void
    {
        $user = User::where('email', config('stockfacil.admin_email'))->firstOrFail();
        $inventory = app(InventoryService::class);
        $items = [
            ['Agua mineral 600 ml', 'BEB-001', 'Bebidas', '3.50', 48, 12, 6],
            ['Refresco de cola 2 L', 'BEB-002', 'Bebidas', '12.00', 18, 6, 4],
            ['Jugo de naranja 1 L', 'BEB-003', 'Bebidas', '9.50', 7, 8, 2],
            ['Papas fritas 100 g', 'SNK-001', 'Snacks', '6.00', 24, 8, 3],
            ['Galletas de avena', 'SNK-002', 'Snacks', '5.50', 4, 5, 1],
            ['Chocolate con leche', 'SNK-003', 'Snacks', '4.00', 0, 5, 6],
            ['Detergente 1 kg', 'LIM-001', 'Limpieza', '18.00', 15, 4, 2],
            ['Lavavajillas 500 ml', 'LIM-002', 'Limpieza', '10.50', 3, 4, 2],
            ['Arroz 1 kg', 'ABA-001', 'Abarrotes', '8.00', 32, 10, 4],
            ['Azúcar 1 kg', 'ABA-002', 'Abarrotes', '7.50', 21, 8, 3],
            ['Jabón de tocador', 'HIG-001', 'Higiene personal', '4.50', 0, 6, 4],
            ['Pasta dental 90 g', 'HIG-002', 'Higiene personal', '12.50', 12, 4, 2],
        ];
        foreach ($items as [$name, $sku, $category, $price, $final, $minimum, $sold]) {
            // Repeated runs preserve edits and real balances.
            DB::transaction(function () use ($inventory, $user, $name, $sku, $category, $price, $final, $minimum, $sold) {
                $category = Category::firstOrCreate(['name' => $category]);
                if (Product::where('sku', $sku)->exists()) {
                    return;
                }
                $product = $inventory->createProduct([
                    'name' => $name, 'sku' => $sku, 'category_id' => $category->id,
                    'price' => $price, 'minimum_stock' => $minimum, 'initial_stock' => $final + $sold,
                    'description' => 'Producto de demostración para una tienda de barrio.',
                ], $user);
                $inventory->record($product, Movement::EXIT, $sold, $user, 'Venta de demostración');
            }, attempts: 5);
        }
    }
}
