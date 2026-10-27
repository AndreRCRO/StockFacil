<?php

namespace Tests\Feature;

use App\Domain\Users\RegistrationData;
use App\Models\User;
use App\Services\RegisterUser;
use Illuminate\Database\UniqueConstraintViolationException;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\ValidationException;
use Tests\TestCase;

class RegistrationPersistenceTest extends TestCase
{
    use RefreshDatabase;

    public function test_service_creates_a_persisted_user_with_normalized_email_and_hidden_hash(): void
    {
        $user = app(RegisterUser::class)->register(new RegistrationData(' Ana SQA ', ' ANA@EXAMPLE.TEST ', 'abc12345'));
        $this->assertTrue($user->exists);
        $this->assertDatabaseCount('users', 1);
        $this->assertDatabaseHas('users', ['id' => $user->id, 'name' => 'Ana SQA', 'email' => 'ana@example.test']);
        $this->assertTrue(Hash::check('abc12345', $user->refresh()->password));
        $this->assertArrayNotHasKey('password', $user->toArray());
    }

    public function test_database_unique_index_rejects_an_exact_duplicate_even_without_validation(): void
    {
        User::factory()->create(['email' => 'ana@example.test']);
        $connection = DB::connection();
        try {
            $connection->table('users')->insert(['name' => 'Duplicada', 'email' => 'ana@example.test', 'password' => 'valor-no-usado']);
            $this->fail('SQLite aceptó un correo idéntico.');
        } catch (UniqueConstraintViolationException) {
            $this->assertDatabaseCount('users', 1);
        }
    }

    public function test_service_rejects_oversized_fields_without_creating_users(): void
    {
        foreach ([
            [str_repeat('a', 121), 'ana@example.test', 'abc12345', 'name'],
            ['Ana', 'ana@example.test', str_repeat('a', 73), 'password'],
            ['Ana', 'ana@example.test', str_repeat('á', 40), 'password'],
        ] as [$name, $email, $password, $field]) {
            try {
                app(RegisterUser::class)->register(new RegistrationData($name, $email, $password));
                $this->fail('El servicio aceptó un campo fuera de límite.');
            } catch (ValidationException $exception) {
                $this->assertArrayHasKey($field, $exception->errors());
            }
        }
        $this->assertDatabaseCount('users', 0);
    }
}
