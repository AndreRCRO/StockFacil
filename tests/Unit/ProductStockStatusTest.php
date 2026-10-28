<?php

namespace Tests\Unit;

use App\Models\Product;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;

class ProductStockStatusTest extends TestCase
{
    #[DataProvider('stockStates')]
    public function test_stock_status_matches_balance_and_minimum(int $stock, string $expected): void
    {
        $product = new Product(['minimum_stock' => 3]);
        $product->stock = $stock;

        $this->assertSame($expected, $product->stock_status);
    }

    public static function stockStates(): array
    {
        return ['agotado' => [0, 'Agotado'], 'inferior' => [2, 'Stock bajo'],
            'minimo exacto' => [3, 'Stock bajo'], 'disponible' => [4, 'Disponible']];
    }
}
