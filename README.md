# Authentication service

Сервис аутентификации на основе jwt токенов. 

## Routes
    Post: 
        /login - выдает пару (<token>, <refresh_token>) токенов по логину и паролю пользователя:
          headers: {"content-type": "application/json"}
          body: {
              "username": <user_login>,
              "password": <user_password_hash>
          }
          response example: {"token": <encoded_jwt_access_token>, "refresh": <encoded_jwt_refresh_token>}
          success code: 200
        
        /refresh - выполняет обновление токенов по истечении времени:
          headers: {"content-type": "application/json"}
          body: {"refresh_token": <encoded_jwt_refresh_token}
          response example: {"token": <encoded_jwt_access_token>, "refresh": <encoded_jwt_refresh_token>}
          success code: 200 
