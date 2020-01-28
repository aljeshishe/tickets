SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));

select count(*) from route;
delete from route where depart!='';
SELECT * FROM tickets.route;
select * from tickets.route order by depart, arrive, carrier_name;
select count(*) from route where carrier_name in ('Wizz Air', 'Ryanair', 'easyJet');
SELECT * FROM route r
  inner join airport a1 on r.depart=a1.code and r.depart=a1.code
  inner join airport a2 on r.arrive=a2.code and r.arrive=a2.code
  where depart='K' # and a2.country_code!='RU'
  and carrier_name in ('Wizz Air', 'Ryanair', 'easyJet', 'Pobeda') ;
select * from route where depart='VKO' and carrier_name in ('Wizz Air', 'Ryanair', 'easyJet', 'Pobeda') ;

SELECT * FROM airport;
SELECT count(*) FROM airport;

show tables;
describe alembic_version;
drop table route;
select * from alembic_version;
select count(*) from ticket;
select * from ticket;
select * from ticket order by price;
select count(*) from ticket where search_date_time < '2018-07-23';
select depart_airport_code, min(price) from ticket group by depart_airport_code;
select * from airport where IATA='LED';

select a1.country, a1.city, a2.city, t.*  from 
  (select depart_airport_code, arrive_airport_code, min(price) as mp from ticket 
    where depart_airport_code='LED' and depart_date_time BETWEEN '2018-08-01' and '2018-09-30' group by arrive_airport_code) as x
  inner join ticket t
    on x.arrive_airport_code=t.arrive_airport_code 
    and x.depart_airport_code=t.depart_airport_code 
    and x.mp=t.price
  inner join airport a1 on x.depart_airport_code=a1.IATA
  inner join airport a2 on x.arrive_airport_code=a2.IATA
  where a2.Country!='Russia'
  order by price;


select * from ticket where depart_airport_code='LED' and depart_date_time BETWEEN '2018-08-01' and '2018-09-30' order by price;
select * from ticket where depart_airport_code='LED' and arrive_airport_code='RHO' and  depart_date_time BETWEEN '2018-08-01' and '2018-09-30' order by price;

select *, min(price) from ticket where depart_airport_code='LED' group by arrive_airport_code;

select * from ticket where depart_date_time > '2018-08-01';

select * from ticket where depart_airport_code='LED' AND arrive_date_time BETWEEN '2018-10-19' AND '2018-10-21' order by price;
select * from ticket where depart_airport_code='CGN' and arrive_airport_code='PMI' AND depart_date_time > '2018-10-20' order by price;
select * from ticket where depart_airport_code='PMI' and arrive_airport_code='BCN' AND depart_date_time > '2018-11-02' and price < 10000;
select * from ticket where depart_airport_code='PMI' AND depart_date_time > '2018-11-02' and price < 4000;
select * from ticket order by price;

select * from ticket where depart_airport_code='CMB' and arrive_airport_code='LED' order by price;
select * from ticket where depart_airport_code='LED' and arrive_airport_code='CMB' order by price;

select * from ticket where depart_airport_code='LPP' order by price;
select * from ticket where arrive_airport_code='LPP' order by price;

select * from ticket where depart_airport_code='PEZ' order by price;
select * from ticket where arrive_airport_code='PEZ' order by price;

select * from ticket where depart_airport_code='LPP' and search_date_time > '2019-03-26 22:20:00' order by price ;
select * from ticket where arrive_airport_code='LPP' and search_date_time > '2019-03-26 22:20:00' order by price ;

select * from ticket where depart_airport_code='ARN' order by price;
select * from ticket where arrive_airport_code='ARN' order by price;

select * from ticket where arrive_airport_code = 'szg' and search_date_time > '2019-03-12 22:20:00'order by price ;
select *, min(price) as m from ticket where search_date_time > '2019-03-12 22:20:00' group by arrive_airport_code order by m ;
select * from ticket where depart_airport_code='LED' and arrive_airport_code='BUD' order by price;

select * from ticket where depart_airport_code='LED' order by price;
select * from ticket where arrive_airport_code='LED' order by price;


select * from ticket where depart_airport_code='PEZ' order by price;
select * from ticket where arrive_airport_code='PEZ' order by price;

select * from ticket where depart_airport_code='CPH' order by price;
select * from ticket where arrive_airport_code='CPH' order by price;

select * from ticket where depart_airport_code='TLL' and arrive_airport_code='GRO' order by price;
select * from ticket where depart_airport_code='GRO' and arrive_airport_code='TLL' order by price;


select * from ticket where depart_airport_code='LPP' and search_date_time > '2019-03-20 22:20:00' order by price ;
select * from ticket where arrive_airport_code='LPP' and search_date_time > '2019-03-20 22:20:00' order by price ;

select * from ticket where depart_airport_code='TLL' and search_date_time > '2019-03-20 22:20:00' order by price ;
select * from ticket where arrive_airport_code='TLL' and search_date_time > '2019-03-20 22:20:00' order by price ;


select * from ticket where arrive_airport_code in ('LED','BUD') and price < 6000 order by depart_date_time;
select * from ticket where depart_airport_code in ('KLV','PRG') order by price;

select * from ticket where arrive_airport_code in ('PFO','LCA','LCN')order by price;
select * from ticket where depart_airport_code in ('PFO','LCA','LCN') order by price;

select * from ticket where arrive_airport_code in ('BRQ','PED','DRS','SXF')order by price;
select * from ticket where depart_airport_code in ('BRQ','PED','DRS','SXF') order by price;

select * from ticket where depart_airport_code='LED' and arrive_airport_code not in ('VKO', 'KGD', 'DME', 'ZIA', 'SVO', 'KZN') and search_date_time > '2019-03-20 22:20:00'  order by price;
select * from ticket where depart_airport_code not in ('VKO', 'KGD', 'DME', 'ZIA', 'SVO', 'KZN') and arrive_airport_code='LED'  and search_date_time > '2019-03-20 22:20:00'  order by price;

select * from ticket where depart_airport_code='DME' and arrive_airport_code='CMB' order by price;
select * from ticket where depart_airport_code='CMB' and arrive_airport_code='DME' order by price;

select * from ticket where depart_airport_code='LED' and arrive_airport_code='BUD' order by price;
select * from ticket where depart_airport_code='BUD' and arrive_airport_code='LED' order by price;

select * from ticket where depart_airport_code='LED' and arrive_airport_code='PEZ' order by price;
select * from ticket where depart_airport_code='PEZ' and arrive_airport_code='LED' order by price;

select * from ticket where depart_airport_code='LED' and arrive_airport_code='PRG' order by price;
select * from ticket where depart_airport_code='PRG' and arrive_airport_code='ZIA' order by price;

select * from ticket where depart_airport_code='CGN' and arrive_airport_code='PMI' order by price;
select * from ticket where arrive_airport_code='PMI' and arrive_date_time < '2018-10-22' order by price;
select * from ticket where depart_airport_code='HEL' and arrive_airport_code='PMI' order by price;
select * from ticket where arrive_airport_code='LTN' order by depart_date_time;
select * from ticket where depart_date_time > '2018-10-10' and depart_airport_code='LED' and price < 10000 order by depart_date_time;
select count(*) from ticket where depart_date_time > '2018-10-10' and depart_airport_code='LED' and price < 10000 order by depart_date_time;
select count(*) from ticket where depart_date_time > '2018-10-10' and price < 10000 order by depart_date_time;
select * from ticket where depart_date_time > '2018-10-10' and price < 10000 order by depart_date_time;
select * from mysql.version;
select * from ticket where depart_date_time < '2018-01-01' order by depart_date_time;
delete from ticket;
DESCRIBE `ticket`;