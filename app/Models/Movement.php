<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Movement extends Model
{
    public const ENTRY = 'entrada';

    public const EXIT = 'salida';

    public $timestamps = false;

    protected $fillable = ['product_id', 'user_id', 'type', 'quantity', 'previous_stock', 'resulting_stock', 'note', 'created_at'];

    protected function casts(): array
    {
        return ['quantity' => 'integer', 'previous_stock' => 'integer', 'resulting_stock' => 'integer', 'created_at' => 'datetime'];
    }

    public function product(): BelongsTo
    {
        return $this->belongsTo(Product::class);
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
