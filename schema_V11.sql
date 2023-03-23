CREATE TABLE "hotel_location" (
  "id" int PRIMARY KEY,
  "hotel_id" int,
  "lat" float,
  "long" float
);

CREATE TABLE "hotel_info" (
  "id" int PRIMARY KEY,
  "name" varchar,
  "neighbourhood" varchar
);

CREATE TABLE "weather_location" (
  "id" int PRIMARY KEY,
  "location_id" int,
  "main_id" int,
  "condition_id" int,
  "dt" timestamp
);

CREATE TABLE "weather_main" (
  "id" int PRIMARY KEY,
  "main" varchar,
  "desc" varchar
);

CREATE TABLE "weather_conditions" (
  "id" int PRIMARY KEY,
  "temperature" float,
  "feels_like" float,
  "clouds" int
);

CREATE TABLE "routes" (
  "id" int PRIMARY KEY,
  "start_location_id" int,
  "end_location_id" int
);

CREATE TABLE "uber_ride" (
  "id" int PRIMARY KEY,
  "route_id" int,
  "time_stamp" timestamp
);

CREATE TABLE "uber_price" (
  "id" int PRIMARY KEY,
  "ride_id" int,
  "x" varchar,
  "green" varchar,
  "assist" varchar,
  "access" varchar,
  "pet" varchar,
  "comfort" varchar,
  "xl" varchar,
  "exec" varchar,
  "lux" varchar
);

CREATE TABLE "train_stations" (
  "id" int PRIMARY KEY,
  "name" varchar,
  "lat" float,
  "long" float
);

CREATE TABLE "tweets" (
  "id" int PRIMARY KEY,
  "text" varchar,
  "edit_history_tweet_ids" int
);

CREATE TABLE "tweet_metadata" (
  "id" int PRIMARY KEY,
  "newest_id" varchar,
  "oldest_id" varchar,
  "result_count" int,
  "tweet_id" int
);

ALTER TABLE "weather_location" ADD FOREIGN KEY ("condition_id") REFERENCES "weather_conditions" ("id");

ALTER TABLE "weather_location" ADD FOREIGN KEY ("main_id") REFERENCES "weather_main" ("id");

ALTER TABLE "hotel_location" ADD FOREIGN KEY ("hotel_id") REFERENCES "hotel_info" ("id");

ALTER TABLE "tweet_metadata" ADD FOREIGN KEY ("tweet_id") REFERENCES "tweets" ("id");

ALTER TABLE "uber_ride" ADD FOREIGN KEY ("route_id") REFERENCES "routes" ("id");

ALTER TABLE "uber_price" ADD FOREIGN KEY ("ride_id") REFERENCES "uber_ride" ("id");

ALTER TABLE "routes" ADD FOREIGN KEY ("start_location_id") REFERENCES "train_stations" ("id");

ALTER TABLE "routes" ADD FOREIGN KEY ("end_location_id") REFERENCES "hotel_location" ("id");

ALTER TABLE "weather_location" ADD FOREIGN KEY ("location_id") REFERENCES "train_stations" ("id");
