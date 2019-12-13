CREATE TABLE "GOOG"
(
  dt timestamp without time zone NOT NULL,
  high numeric NOT NULL,
  low numeric NOT NULL,
  open numeric NOT NULL,
  close numeric NOT NULL,
  volume numeric NOT NULL,
  adj_close numeric NOT NULL
  CONSTRAINT "GOOG_pkey" PRIMARY KEY (dt)
);