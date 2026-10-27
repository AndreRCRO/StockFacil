<?php

namespace Tests\Unit;

use App\Domain\Users\RegistrationData;
use PHPUnit\Framework\TestCase;

class RegistrationDataTest extends TestCase
{
    public function test_valid_registration_data_is_ready_to_create_a_user(): void
    {
        $data = new RegistrationData('Ana SQA', 'ana@example.test', 'abc12345');

        $this->assertSame('Ana SQA', $data->name);
        $this->assertSame('ana@example.test', $data->email);
        $this->assertSame('abc12345', $data->password);
    }

    public function test_registration_normalizes_name_and_email(): void
    {
        $data = new RegistrationData(' Ana SQA ', ' ANA@EXAMPLE.TEST ', 'abc12345');

        $this->assertSame('Ana SQA', $data->name);
        $this->assertSame('ana@example.test', $data->email);
    }
}
