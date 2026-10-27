<?php

namespace Tests\Feature;

use App\Models\Category;
use App\Models\User;
use App\Services\InventoryService;
use Illuminate\Support\Facades\DB;
use Symfony\Component\Process\Process;
use Tests\TestCase;

class ConcurrencyTest extends TestCase
{
    public function test_simultaneous_exits_cannot_oversell_and_history_remains_consistent(): void
    {
        $path = tempnam(sys_get_temp_dir(), 'stockfacil-test-');
        $previous = config('database.connections.sqlite.database');
        try {
            config(['database.connections.sqlite.database' => $path]);
            DB::purge('sqlite');
            $this->artisan('migrate', ['--force' => true])->assertExitCode(0);
            $user = User::factory()->create();
            $category = Category::create(['name' => 'Prueba']);
            $product = app(InventoryService::class)->createProduct(['name' => 'Prueba concurrente', 'sku' => 'CON-001', 'category_id' => $category->id, 'price' => 1, 'initial_stock' => 10, 'minimum_stock' => 3], $user);
            $startAt = (string) (microtime(true) + 1.5);
            $command = [PHP_BINARY, base_path('tests/Support/concurrent-movement.php'), $path, (string) $product->id, (string) $user->id, $startAt];
            $first = new Process($command, base_path(), timeout: 20);
            $second = new Process($command, base_path(), timeout: 20);
            $first->start();
            $second->start();
            $first->wait();
            $second->wait();
            $codes = [$first->getExitCode(), $second->getExitCode()];
            sort($codes);
            $this->assertSame([0, 2], $codes, $first->getErrorOutput().$second->getErrorOutput());
            $this->assertSame(3, $product->refresh()->stock);
            $this->assertDatabaseCount('movements', 2);
            $this->assertDatabaseHas('movements', ['type' => 'salida', 'quantity' => 7, 'previous_stock' => 10, 'resulting_stock' => 3]);
        } finally {
            DB::disconnect('sqlite');
            config(['database.connections.sqlite.database' => $previous]);
            DB::purge('sqlite');
            foreach ([$path, $path.'-wal', $path.'-shm'] as $file) {
                if (is_file($file)) {
                    unlink($file);
                }
            }
        }
    }
}
