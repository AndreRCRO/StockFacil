# language: es
Característica: Registro de usuario en StockFácil
  Como nuevo usuario del sistema local
  Quiero crear una cuenta con mi correo
  Para acceder al inventario compartido

  # CA-R01; RegistrationTest::test_valid_registration_persists_hashed_password_and_allows_login
  Escenario: Crear una cuenta con datos válidos
    Dado que no existe una cuenta con el correo "ana@example.test"
    Y que ingreso el nombre "Ana SQA"
    Y que ingreso el correo "ana@example.test"
    Y que ingreso la contraseña "abc12345" y su confirmación coincidente
    Cuando confirmo el registro
    Entonces el sistema crea una sola cuenta
    Y almacena la contraseña de forma protegida
    Y veo "Cuenta creada correctamente. Ya puedes iniciar sesión."
    Y puedo iniciar sesión con esa cuenta

  # CA-R02; RegistrationTest::test_duplicate_email_is_rejected_case_insensitively
  Escenario: Intento de registro con correo duplicado
    Dado que existe un usuario con el correo "ana@example.test"
    Cuando intento registrarme con el correo " ANA@EXAMPLE.TEST " y demás datos válidos
    Entonces veo "Este correo electrónico ya está registrado."
    Y se conserva una sola cuenta con ese correo

