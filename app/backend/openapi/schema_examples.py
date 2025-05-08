class DeviceSchemas:
    DEVICE = {
        "examples": [
            {
                "id": 1,
                "name": "XPS 13",
                "brand": "Dell",
                "price": 1299.99
            }
        ]
    }

    DEVICE_CREATE = {
        "examples": [
            {
                "name": "XPS 13",
                "brand": "Dell",
                "price": 1299.99
            }
        ]
    }

    DEVICE_FILTER_RESULT = {
        "examples": [
            {
                "items": [
                    {
                        "name": "iPhone 13",
                        "brand": "Apple",
                        "price": 999
                    },
                    {
                        "name": "Samsung Galaxy S21",
                        "brand": "Samsung",
                        "price": 899
                    }
                ],
                "total": 2
            }
        ]
    }

    USER_DEVICE_CART = {
        "examples": [
            {
                "items": [
                    {
                        "name": "Smartphone X",
                        "brand": "TechBrand",
                        "quantity": 2,
                        "price": 399.99
                    },
                    {
                        "name": "Laptop Pro",
                        "brand": "CompTech",
                        "quantity": 1,
                        "price": 1299.99
                    }
                ]
            }
        ]
    }

    CART_PURCHASE_RESULT = {
        "examples": [
            {
                "purchasedItems": [
                    {
                        "name": "Smartphone X",
                        "brand": "TechBrand",
                        "unitPrice": 399.99,
                        "quantity": 2,
                        "totalPrice": 799.98
                    },
                    {
                        "name": "Laptop Pro",
                        "brand": "CompTech",
                        "unitPrice": 1299.99,
                        "quantity": 1,
                        "totalPrice": 1299.99
                    }
                ],
                "totalPurchasePrice": 2099.97
            }
        ]
    }


class AuthSchemas:
    LOGIN_REQUEST = {
        "examples": [
            {
                "email": "user@example.com",
                "password": "pa$$w0rd123"
            }
        ]
    }

    TOKEN_PAIR = {
        "examples": [
            {
                "access_token": "eyJhbGciOiJIUzI1...",
                "refresh_token": "eyJhbGciOiJIUzI1..."
            }
        ]
    }

    ACCESS_TOKEN = {
        "examples": [
            {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        ]
    }

    REFRESH_TOKEN = {
        "examples": [
            {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        ]
    }

    SUCCESS_RESPONSE = {
        "examples": [
            {
                "message": "Регистрация прошла успешно",
                "userId": "123e4567-e89b-12d3-a456-426614174000"
            }
        ]
    }

    SIGNUP_REQUEST = {
        "examples": [
            {
                "email": "example@domain.com",
                "password": "Password123"
            }
        ]
    }
