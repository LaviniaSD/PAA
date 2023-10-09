class InvalidColumnError(Exception):
    """Exceção levantada quando uma coluna específica não é suportada como parâmetro de uma função.
    """

    def __init__(self, message="A coluna informada não é suportada pela função", column=None):
        """Construtor da classe.

        Args:
            message (str, optional): Mensagem de erro. Defaults to "A coluna informada não é suportada pela função".
            column (str, optional): Nome da coluna. Defaults to None.
        """

        # Caso o usuário informe a coluna, adiciona a coluna à mensagem de erro
        if column is not None:
            message = f"{message}: {column}"

        self.message = message
        self.column = column
        super().__init__(self.message)

raise InvalidColumnError("A coluna informada não é suportada pela função", column="id")