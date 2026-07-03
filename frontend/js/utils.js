function normalizarCategoria(categoria) {
    if (!categoria && categoria !== 0) {
        return "Burgers";
    }

    const categoriaTexto = String(categoria).trim().toLowerCase();

    const mapaCategorias = {
        "1": "Burgers",
        "burgers": "Burgers",
        "burger": "Burgers",
        "2": "Pizza",
        "pizza": "Pizza",
        "3": "Vegetariano",
        "vegetariano": "Vegetariano",
        "vegetarian": "Vegetariano",
        "4": "Kids",
        "kids": "Kids",
        "kid": "Kids"
    };

    return mapaCategorias[categoriaTexto] || (['Burgers', 'Pizza', 'Vegetariano', 'Kids']
        .includes(categoria) ? categoria : 'Burgers');
}