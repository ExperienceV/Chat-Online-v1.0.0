from functions_jwt import validate_token
import json
from dotenv import load_dotenv

load_dotenv('.env')

tk = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NCwidXNlcl9uYW1lIjoiSXNhIiwidXNlcl9wYXNzd29yZCI6IjEyMyIsImV4cCI6MTcyNTI5MTAwN30.EEVR1TDFxR_FdR5mbZedozSxVXq0qL7SX-gFWih-x28"

def find_name(token):
    verify_token_response = validate_token(token=token, output=True)
    print(json.loads(verify_token_response.body.decode("UTF-8")))
    #return verify_token_response
    #db_response = await user_data()

find_name(tk)