from passlib.hash import bcrypt
print(bcrypt.using(ident="2a").hash(''))
