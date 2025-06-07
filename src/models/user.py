from dataclasses import dataclass

@dataclass
class User:
    """Modelo para representar um usuário"""
    user_id: str
    first_name: str
    email: str
    phone_number: str = None

    def has_valid_phone(self) -> bool:
        """Verifica se o usuário tem um número de telefone válido"""
        return bool(self.phone_number) 