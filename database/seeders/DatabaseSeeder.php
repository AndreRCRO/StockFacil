<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        User::updateOrCreate(['email' => config('stockfacil.admin_email')], [
            'name' => config('stockfacil.admin_name'), 'password' => config('stockfacil.admin_password'),
        ]);
        $this->call(DemoInventorySeeder::class);
    }
}
