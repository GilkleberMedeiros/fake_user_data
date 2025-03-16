# API

My first fastapi api. 
Returns user fake data: Name="first last", email="l.first@gmail.com" and password="TOKEN_HEX_16".

visit '/docs' to see auto generated docs :).


## Usage
request under '/'

query params:
    - n: int, required, number of fake users returned.
    - unique: bool, optional, default=true, if it will generate only unique names.