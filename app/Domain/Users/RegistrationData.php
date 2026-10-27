<?php

namespace App\Domain\Users;

use App\Support\EmailNormalizer;

final readonly class RegistrationData
{
    public string $name;

    public string $email;

    public function __construct(
        string $name,
        string $email,
        public string $password,
    ) {
        $this->name = trim($name);
        $this->email = EmailNormalizer::normalize($email);
    }
}
