<?php

namespace App\Services;

use App\Models\Movement;
use App\Models\Product;
use App\Models\User;
use Illuminate\Support\Facades\DB;
use Illuminate\Validation\ValidationException;

class InventoryService
{
    public function createProduct(array $data, User $user): Product
    {
        $initialStock = (int) $data['initial_stock'];
        if ($initialStock < 0 || $initialStock > Product::MAX_STOCK) {
            throw ValidationException::withMessages(['initial_stock' => 'El stock inicial está fuera del rango permitido.']);
        }

        return DB::transaction(function () use ($data, $initialStock, $user) {
            unset($data['initial_stock'], $data['stock'], $data['is_active']);
            $product = Product::create($data);
            if ($initialStock > 0) {
                $this->record($product, Movement::ENTRY, $initialStock, $user, 'Stock inicial');
            }

            return $product->refresh();
        }, attempts: 5);
    }

    public function record(Product $product, string $type, int $quantity, User $user, ?string $note = null): Movement
    {
        if (! in_array($type, [Movement::ENTRY, Movement::EXIT], true)) {
            throw ValidationException::withMessages(['type' => 'Selecciona una entrada o salida.']);
        }
        if ($quantity <= 0 || $quantity > Product::MAX_STOCK) {
            throw ValidationException::withMessages(['quantity' => 'La cantidad debe ser un entero positivo dentro del rango permitido.']);
        }

        return DB::transaction(function () use ($product, $type, $quantity, $user, $note) {
            // PHP 8.3 uses DEFERRED transactions even with Laravel's IMMEDIATE setting.
            // Make the first statement a write: SQLite locks writers before we read the balance.
            DB::table('products')->where('id', $product->id)->update(['stock' => DB::raw('stock')]);
            $current = Product::findOrFail($product->id);
            if (! $current->is_active) {
                throw ValidationException::withMessages(['product_id' => 'El producto está inactivo. Selecciona un producto activo.']);
            }
            $previous = $current->stock;
            $next = $previous + ($type === Movement::ENTRY ? $quantity : -$quantity);
            if ($next < 0) {
                throw ValidationException::withMessages(['quantity' => "Stock insuficiente. Solo hay {$previous} unidades disponibles."]);
            }
            if ($next > Product::MAX_STOCK) {
                throw ValidationException::withMessages(['quantity' => 'La entrada supera el límite de unidades permitido.']);
            }
            // A conditional write also prevents overwriting a newer balance with a stale read.
            $updated = Product::whereKey($current->id)->where('is_active', true)->where('stock', $previous)
                ->update(['stock' => $next, 'updated_at' => now()]);
            if ($updated !== 1) {
                throw ValidationException::withMessages(['quantity' => 'El inventario cambió. Actualiza la página e intenta nuevamente.']);
            }

            return Movement::create([
                'product_id' => $current->id, 'user_id' => $user->id, 'type' => $type,
                'quantity' => $quantity, 'previous_stock' => $previous, 'resulting_stock' => $next,
                'note' => $note, 'created_at' => now(),
            ]);
        }, attempts: 5);
    }
}
