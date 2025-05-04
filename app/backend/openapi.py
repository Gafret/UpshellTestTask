from starlette.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, \
    HTTP_200_OK, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR

from app.schemas.base import ErrorResponse


class AuthRouteResponses:
    refresh_responses = {
        HTTP_200_OK: {"description": "Успешный ответ с новым access-токеном"},
        HTTP_400_BAD_REQUEST: {"description": "Неверный запрос",
                               "content": {
                                   "application/json": {
                                       "examples": {
                                           "Токен отсутствует": {
                                               "value": {
                                                   "error": "Отсутствует refresh-токен в запросе."},
                                           },
                                       }
                                   }
                               },
                               "model": ErrorResponse},
        HTTP_401_UNAUTHORIZED: {"description": "Неавторизован (refresh-токен недействителен)",
                                "content": {
                                    "application/json": {
                                        "examples": {
                                            "Недействительный токен": {
                                                "value": {
                                                    "error": "Refresh-токен недействителен или истёк."},
                                            },
                                        }
                                    }
                                },
                                "model": ErrorResponse},
    }

    login_responses = {
        HTTP_200_OK: {"description": "Успешная аутентификация"},
        HTTP_400_BAD_REQUEST: {"description": "Ошибка в запросе",
                               "content": {
                                   "application/json": {
                                       "examples": {
                                           "Неверный формат email": {
                                               "value": {
                                                   "error": "Неверный формат email"},
                                           },
                                       }
                                   }
                               },
                               "model": ErrorResponse},
        HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Внутренняя ошибка сервера",
                                         "content": {
                                             "application/json": {
                                                 "examples": {
                                                     "Серверная ошибка": {
                                                         "value": {
                                                             "error": "Произошла ошибка на сервере. Попробуйте позже."},
                                                     },
                                                 }
                                             }
                                         },
                                         "model": ErrorResponse},
    }

    register_responses = {
        HTTP_201_CREATED: {"description": "Пользователь успешно зарегистрирован"},
        HTTP_400_BAD_REQUEST: {"description": "Некорректные данные запроса",
                               "content": {
                                   "application/json": {
                                       "examples": {
                                           "Некорректный формат почты": {
                                               "value": {
                                                   "error": "Некорректный формат электронной почты"},
                                           },
                                       }
                                   }
                               },
                               "model": ErrorResponse},
        HTTP_409_CONFLICT: {"description": "Пользователь уже зарегистрирован",
                            "content": {
                                "application/json": {
                                    "examples": {
                                        "Уже существует": {
                                            "value": {
                                                "error": "Пользователь с таким email уже зарегистрирован"},
                                        },
                                    }
                                }
                            },
                            "model": ErrorResponse},
        HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Внутренняя ошибка сервера",
                                         "content": {
                                             "application/json": {
                                                 "examples": {
                                                     "Серверная ошибка": {
                                                         "value": {
                                                             "error": "Произошла ошибка на сервере. Попробуйте позже."},
                                                     },
                                                 }
                                             }
                                         },
                                         "model": ErrorResponse},
    }


class DevicesRouteResponses:
    add_device_responses = {
        HTTP_201_CREATED: {"description": "Товар успешно добавлен в каталог."},
        HTTP_400_BAD_REQUEST: {"description": "Ошибка в запросе. Некорректные данные.",
                               "content": {
                                   "application/json": {
                                       "examples": {
                                           "Ошибка заполнения (недостающее поле)": {
                                               "value": {
                                                   "error": "Поле name обязательно для заполнения"},
                                           },
                                       }
                                   }
                               },
                               "model": ErrorResponse},
        HTTP_401_UNAUTHORIZED: {"description": "Неавторизованный доступ. Требуется Bearer токен.",
                                "content": {
                                    "application/json": {
                                        "examples": {
                                            "Неавторизованный пользователь": {
                                                "value": {
                                                    "error": "Неавторизованный пользователь"},
                                            },
                                        }
                                    }
                                },
                                "model": ErrorResponse},
        HTTP_403_FORBIDDEN: {"description": "Доступ запрещен. Недостаточно прав.",
                             "content": {
                                 "application/json": {
                                     "examples": {
                                         "У пользователя нет прав": {
                                             "value": {
                                                 "error": "Пользователь не имеет прав доступа для этой операции"},
                                         },
                                     }
                                 }
                             },
                             "model": ErrorResponse},
    }
    devices_responses = {
        HTTP_200_OK: {"description": "Список устройств"},
        HTTP_400_BAD_REQUEST: {"description": "Ошибка в запросе",
                               "content": {
                                   "application/json": {
                                       "examples": {
                                           "Неверный диапазон цен": {
                                               "value": {
                                                   "error": "Максимальная цена не может быть меньше минимальной цены"},
                                           },
                                       }
                                   }
                               },
                               "model": ErrorResponse},
    }
    buy_responses = {
        HTTP_200_OK: {"description": "Успешная покупка"},
        HTTP_400_BAD_REQUEST: {"description": "Некорректный запрос",
                               "content": {
                                   "application/json": {
                                       "examples": {
                                           "Некорректное количество": {
                                               "value": {"error": "Некорректное количество товара"},
                                           },
                                       }
                                   }
                               },
                               "model": ErrorResponse},
        HTTP_401_UNAUTHORIZED: {"description": "Неавторизованный пользователь",
                                "content": {
                                    "application/json": {
                                        "examples": {
                                            "Неавторизованный пользователь": {
                                                "value": {"error": "Неавторизованный пользователь"},
                                            },
                                        }
                                    }
                                },
                                "model": ErrorResponse},
    }
