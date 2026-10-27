<?php

namespace Tests\Unit;

use App\Support\EmailNormalizer;
use PHPUnit\Framework\TestCase;

class EmailNormalizerTest extends TestCase
{
    public function test_email_has_the_same_canonical_value_with_case_and_outer_spaces(): void
    {
        foreach (['ana@example.test', 'ANA@EXAMPLE.TEST', ' ANA@EXAMPLE.TEST ', "\tAna@Example.Test\n"] as $email) {
            $this->assertSame('ana@example.test', EmailNormalizer::normalize($email));
        }
    }
}
