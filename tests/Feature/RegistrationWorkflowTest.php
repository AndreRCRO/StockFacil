<?php

namespace Tests\Feature;

use App\Domain\Users\RegistrationData;
use App\Models\User;
use App\Services\RegisterUser;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\ValidationException;
use Tests\TestCase;

class RegistrationWorkflowTest extends TestCase
{
    use RefreshDatabase;

    public function test_registration_contract_creates_one_account_and_allows_authentication(): void
    {
        $this->assertDatabaseCount('users', 0);
        $this->post('/register', [
            'name' => 'Ana SQA',
            'email' => ' ANA@EXAMPLE.TEST ',
            'password' => 'abc12345',
            'password_confirmation' => 'abc12345',
        ])->assertRedirect('/login')->assertSessionHas('status', 'Cuenta creada correctamente. Ya puedes iniciar sesión.');
        $this->assertDatabaseCount('users', 1);
        $user = User::firstOrFail();
        $this->assertSame('Ana SQA', $user->name);
        $this->assertSame('ana@example.test', $user->email);
        $this->assertNotSame('abc12345', $user->password);
        $this->assertTrue(Hash::check('abc12345', $user->password));
        $this->assertGuest();
        $this->post('/login', ['email' => ' ANA@EXAMPLE.TEST ', 'password' => 'abc12345'])->assertRedirect('/dashboard');
        $this->assertAuthenticatedAs($user);
        $this->get('/dashboard')->assertOk();
    }

    public function test_registration_service_rejects_short_password_without_creating_user(): void
    {
        try {
            app(RegisterUser::class)->register(new RegistrationData('Ana SQA', 'ana@example.test', '1234567'));
            $this->fail('El servicio creó una cuenta con una contraseña de siete caracteres.');
        } catch (ValidationException $exception) {
            $this->assertArrayHasKey('password', $exception->errors());
        }
        $this->assertDatabaseCount('users', 0);
    }

    public function test_registration_service_rejects_invalid_name_and_email(): void
    {
        foreach ([['', 'ana@example.test', 'name'], ['Ana SQA', 'no-es-correo', 'email']] as [$name, $email, $field]) {
            try {
                app(RegisterUser::class)->register(new RegistrationData($name, $email, 'abc12345'));
                $this->fail('El servicio aceptó datos inválidos: '.$field);
            } catch (ValidationException $exception) {
                $this->assertArrayHasKey($field, $exception->errors());
            }
        }
        $this->assertDatabaseCount('users', 0);
    }

    public function test_existing_noncanonical_email_cannot_be_registered_again(): void
    {
        User::factory()->create(['email' => ' ANA@EXAMPLE.TEST ']);
        $this->from('/register')->post('/register', [
            'name' => 'Otra Ana', 'email' => 'ana@example.test',
            'password' => 'abc12345', 'password_confirmation' => 'abc12345',
        ])->assertRedirect('/register')->assertSessionHasErrors('email');
        $this->assertDatabaseCount('users', 1);
        $this->assertDatabaseHas('users', ['email' => ' ANA@EXAMPLE.TEST ']);
    }
}
