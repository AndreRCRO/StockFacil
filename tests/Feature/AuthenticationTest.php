<?php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Hash;
use Tests\TestCase;

class AuthenticationTest extends TestCase
{
    use RefreshDatabase;

    public function test_internal_routes_require_authentication(): void
    {
        foreach (['/dashboard', '/products', '/products/create', '/movements', '/movements/create', '/stock-bajo'] as $url) {
            $this->get($url)->assertRedirect(route('login'));
        }
        $this->post('/products', [])->assertRedirect(route('login'));
        $this->post('/movements', [])->assertRedirect(route('login'));
        $this->assertDatabaseCount('products', 0);
    }

    public function test_login_and_logout(): void
    {
        $user = User::factory()->create(['password' => 'ClaveLocal123!']);
        $this->assertTrue(Hash::check('ClaveLocal123!', $user->password));
        $this->get(route('login'))->assertOk()->assertSee('Iniciar sesión');
        $this->post(route('login.store'), ['email' => $user->email, 'password' => 'ClaveLocal123!'])->assertRedirect(route('dashboard'));
        $this->assertAuthenticatedAs($user);
        $this->get(route('login'))->assertRedirect(route('dashboard'));
        $this->post(route('logout'))->assertRedirect(route('login'));
        $this->assertGuest();
        $this->get(route('dashboard'))->assertRedirect(route('login'));
    }

    public function test_invalid_credentials_and_login_throttling(): void
    {
        $user = User::factory()->create();
        for ($i = 0; $i < 5; $i++) {
            $this->post(route('login.store'), ['email' => $user->email, 'password' => 'invalid'])->assertSessionHasErrors('email');
        }
        $this->followingRedirects()->from(route('login'))->post(route('login.store'), ['email' => $user->email, 'password' => 'password'])->assertSee('Demasiados intentos');
        $this->assertGuest();
    }

    public function test_public_registration_is_available(): void
    {
        $this->get('/register')->assertOk()->assertSee('Crear cuenta');
        $this->post('/register')->assertSessionHasErrors(['name', 'email', 'password']);
    }
}
