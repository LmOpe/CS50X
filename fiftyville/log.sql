-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Get information from the crime scene report
SELECT description FROM crime_scene_reports 
-- The day of crime
WHERE year = "2021" AND month = "7" AND day = "28"
-- It occured on Humphrey street
AND street = "Humphrey Street";

--Get the interview information
SELECT transcript FROM interviews
-- The day of crime
WHERE year = "2021" AND month = "7" AND day = "28";

-- Get the names and filters it with the interview information till we get the thief's name
    SELECT name FROM people
    -- Information from security logs
    WHERE people.license_plate IN (
        -- Get the license plates from bakery security logs
        SELECT license_plate FROM bakery_security_logs
        -- In the ten minutes time frame
        WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute > 15 AND minute < 25
    )
        -- Get information from phone calls 
        AND people.phone_number IN (
            -- Get the phone number
            SELECT caller FROM phone_calls
        -- Date of the crime 
        WHERE year = 2021 AND month = 7 AND day = 28
        -- Call duration less than a minute 
        AND duration < 60
        )
        -- Get information from bank accounts
        AND people.id IN (
            -- Get person id from bank account
            SELECT person_id FROM bank_accounts
            -- Join bank account information with the transactions details to get the person id
        JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
        -- Transaction was on the day the crime occured 
        WHERE atm_transactions.year = 2021 AND atm_transactions.month = 7 AND atm_transactions.day = 28
        -- It was a withdrawal 
        AND atm_transactions.transaction_type = "withdraw"
        -- It occured on Leggett Street
        AND atm_transactions.atm_location = "Leggett Street"
        )
        -- Get infornmation from flight passenger list
        AND people.passport_number IN (
            -- Get the passport number of the passengers
            SELECT passport_number FROM passengers
            -- Get the id of the first flight 
            WHERE flight_id IN (
        -- Get the flight id from flights
        SELECT id FROM flights
        -- The first flight on the second day of crime
        WHERE year = 2021 AND month = 7 AND day = 29 ORDER BY hour ASC LIMIT 1
        )
    );

-- Get city name
SELECT city FROM airports
-- Get flight id
WHERE id IN (
    -- From the first flight of the day
    SELECT destination_airport_id FROM flights
    WHERE year = 2021 AND month = 7 AND day = 29 ORDER BY hour, minute ASC LIMIT 1
);

-- Get the accomplice's name
SELECT name FROM people WHERE phone_number IN (
    -- Get the phone number
SELECT receiver FROM phone_calls
-- The day of crime
WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60
-- Filter with criminal's phone number
AND caller == (SELECT phone_number FROM people WHERE name = "Bruce")
);