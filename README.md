# Wallet Service
 
WalletService provides a fund transfer solution across MovileWallet's user base.

## Assumptions

### Business ones

1. User has only one account (TODO: introduce multiple account for user)
2. 'amount' is an integer, not to hassle with cents for simplicity.
3. 'amount' shall be a positive number and less than 1000000 SGD.
4. No double-entry accounting, more simple data model
5. No notification (but it's a good feature proposal - notify users about received money transfer)
6. 'user_id' is a string, like username or email.

### Technical
1. No User and Auth service, I assume there is sessions stored in redis (populates manually)
2. Authentication based on token (session), which generated on login.
3. asyncio from sqlalchemy 1.4?

## How to start up

## Data model

## API

## Design

Stack: python, fastapi, sqlalchemy, alembic, postgres, redis.

### Security

### Observability

#### Logging

#### Monitoring

## Estimations

### Data

### Performance
