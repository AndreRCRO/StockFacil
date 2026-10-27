<?php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Hash;
use Tests\TestCase;

class RegistrationTest extends TestCase
{
    use RefreshDatabase;

    private function data(array $overrides = []): array
    {
        return array_replace(['name' => 'Ana SQA', 'email' => 'ana@example.test', 'password' => 'abc12345', 'password_confirmation' => 'abc12345'], $overrides);
    }

    public function test_valid_registration_persists_hashed_password_and_allows_login(): void
    {
        $this->get('/register')->assertOk()->assertSee('Crear cuenta');
        $this->post('/register', $this->data())->assertRedirect('/login')->assertSessionHas('status');
        $this->assertDatabaseCount('users', 1);
        $user = User::firstOrFail();
        $this->assertTrue(Hash::check('abc12345', $user->password));
        $this->assertNotSame('abc12345', $user->password);
        $this->assertGuest();
        $this->post('/login', ['email' => 'ana@example.test', 'password' => 'abc12345'])->assertRedirect('/dashboard');
        $this->assertAuthenticatedAs($user);
    }

    public function test_duplicate_email_is_rejected_case_insensitively(): void
    {
        User::factory()->create(['email' => 'ana@example.test']);
        $this->from('/register')->post('/register', $this->data(['email' => ' ANA@EXAMPLE.TEST ']))->assertRedirect('/register')->assertSessionHasErrors('email');
        $this->assertDatabaseCount('users', 1);
    }

    public function test_registered_user_can_login_with_uppercase_email(): void
    {
        $this->post('/register', $this->data())->assertRedirect('/login');
        $this->post('/login', ['email' => ' ANA@EXAMPLE.TEST ', 'password' => 'abc12345'])->assertRedirect('/dashboard');
        $this->assertAuthenticated();
    }

    public function test_invalid_inputs_are_rejected_without_persisting_users(): void
    {
        foreach ([['name' => ''], ['email' => 'invalido'], ['password' => '1234567', 'password_confirmation' => '1234567'], ['password_confirmation' => 'diferente'], ['email' => ['array']], ['name' => ['array']], ['password' => str_repeat('á', 40), 'password_confirmation' => str_repeat('á', 40)]] as $overrides) {
            $this->from('/register')->post('/register', $this->data($overrides))->assertRedirect('/register')->assertSessionHasErrors();
            $this->assertDatabaseCount('users', 0);
            $this->assertGuest();
        }
    }

    public function test_email_is_normalized_and_password_is_not_flushed_to_old_input(): void
    {
        $this->from('/register')->post('/register', $this->data(['name' => '', 'email' => ' ANA@EXAMPLE.TEST ']))->assertSessionHasErrors('name')->assertSessionMissing('_old_input.password')->assertSessionMissing('_old_input.password_confirmation');
        $this->post('/register', $this->data(['email' => ' ANA@EXAMPLE.TEST ']))->assertRedirect('/login');
        $this->assertDatabaseHas('users', ['email' => 'ana@example.test']);
    }

    public function test_authenticated_user_cannot_register_another_account(): void
    {
        $this->actingAs(User::factory()->create());
        $this->get('/register')->assertRedirect('/dashboard');
        $this->post('/register', $this->data())->assertRedirect('/dashboard');
        $this->assertDatabaseCount('users', 1);
    }

    public function test_registration_is_limited_to_ten_posts_per_minute(): void
    {
        for ($attempt = 0; $attempt < 10; $attempt++) {
            $this->post('/register', [])->assertSessionHasErrors();
        }
        $this->post('/register', [])->assertStatus(429);
        $this->assertDatabaseCount('users', 0);
    }
}
