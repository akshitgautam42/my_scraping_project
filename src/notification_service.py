class ConsoleNotifier:
    def send(self, product_count: int):
        print(f"Successfully scraped and updated {product_count} products in the database.")
