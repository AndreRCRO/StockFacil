<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('categories', function (Blueprint $table) {
            $table->id();
            $table->string('name')->unique();
            $table->timestamps();
        });
        Schema::create('products', function (Blueprint $table) {
            $table->id();
            $table->foreignId('category_id')->constrained()->restrictOnDelete();
            $table->string('name', 150);
            $table->string('sku', 60)->unique();
            $table->text('description')->nullable();
            $table->decimal('price', 12, 2);
            $table->unsignedInteger('stock')->default(0);
            $table->unsignedInteger('minimum_stock')->default(0);
            $table->boolean('is_active')->default(true)->index();
            $table->timestamps();
        });
        Schema::create('movements', function (Blueprint $table) {
            $table->id();
            $table->foreignId('product_id')->constrained()->restrictOnDelete();
            $table->foreignId('user_id')->constrained()->restrictOnDelete();
            $table->string('type', 10);
            $table->unsignedInteger('quantity');
            $table->unsignedInteger('previous_stock');
            $table->unsignedInteger('resulting_stock');
            $table->text('note')->nullable();
            $table->timestamp('created_at');
            $table->index(['product_id', 'created_at']);
            $table->index(['type', 'created_at']);
        });
        // SQLite does not enforce unsigned integers; guard the database too.
        DB::unprepared("CREATE TRIGGER products_valid_insert BEFORE INSERT ON products WHEN NEW.stock < 0 OR NEW.stock > 2147483647 OR NEW.minimum_stock < 0 OR NEW.price < 0 BEGIN SELECT RAISE(ABORT, 'Invalid product values'); END");
        DB::unprepared("CREATE TRIGGER products_valid_update BEFORE UPDATE ON products WHEN NEW.stock < 0 OR NEW.stock > 2147483647 OR NEW.minimum_stock < 0 OR NEW.price < 0 BEGIN SELECT RAISE(ABORT, 'Invalid product values'); END");
        DB::unprepared("CREATE TRIGGER movements_valid_insert BEFORE INSERT ON movements WHEN NEW.quantity <= 0 OR NEW.previous_stock < 0 OR NEW.resulting_stock < 0 OR NEW.type NOT IN ('entrada', 'salida') OR (NEW.type = 'entrada' AND NEW.resulting_stock != NEW.previous_stock + NEW.quantity) OR (NEW.type = 'salida' AND NEW.resulting_stock != NEW.previous_stock - NEW.quantity) BEGIN SELECT RAISE(ABORT, 'Invalid movement values'); END");
    }

    public function down(): void
    {
        Schema::dropIfExists('movements');
        Schema::dropIfExists('products');
        Schema::dropIfExists('categories');
    }
};
