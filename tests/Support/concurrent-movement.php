<?php

use App\Models\Movement;
use App\Models\Product;
use App\Models\User;
use App\Services\InventoryService;
use Illuminate\Contracts\Console\Kernel;
use Illuminate\Support\Facades\DB;
use Illuminate\Validation\ValidationException;

// This worker is only launched against the temporary test database.
require __DIR__.'/../../vendor/autoload.php';
$app = require __DIR__.'/../../bootstrap/app.php';
$app->make(Kernel::class)->bootstrap();
config(['database.connections.sqlite.database' => $argv[1], 'cache.default' => 'array']);
DB::purge('sqlite');
while (microtime(true) < (float) $argv[4]) {
    usleep(1000);
}
try {
    app(InventoryService::class)->record(
        Product::findOrFail($argv[2]),
        Movement::EXIT,
        7,
        User::findOrFail($argv[3]),
        'Salida concurrente de prueba',
    );
    echo 'accepted';
} catch (ValidationException $exception) {
    echo 'rejected';
    exit(2);
}
