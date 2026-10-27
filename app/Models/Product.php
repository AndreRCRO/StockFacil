<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Product extends Model
{
    public const MAX_STOCK = 2147483647;

    // Only InventoryService changes stock.
    protected $fillable = ['name', 'sku', 'category_id', 'description', 'price', 'minimum_stock', 'is_active'];

    protected function casts(): array
    {
        return ['price' => 'decimal:2', 'stock' => 'integer', 'minimum_stock' => 'integer', 'is_active' => 'boolean'];
    }

    public function category(): BelongsTo
    {
        return $this->belongsTo(Category::class);
    }

    public function movements(): HasMany
    {
        return $this->hasMany(Movement::class);
    }

    public function scopeActive(Builder $query): Builder
    {
        return $query->where('is_active', true);
    }

    public function scopeLowStock(Builder $query): Builder
    {
        return $query->active()->whereColumn('stock', '<=', 'minimum_stock');
    }

    public function getStockStatusAttribute(): string
    {
        return $this->stock === 0 ? 'Agotado' : ($this->stock <= $this->minimum_stock ? 'Stock bajo' : 'Disponible');
    }
}
