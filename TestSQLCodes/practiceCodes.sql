
/* Union: basically to combine columns from 2 tables */
/* ex: grab City from Customers and Suppliers tables,
then order the City by the City */

SELECT City FROM Customers
Union
SELECT City FROM Suppliers
order by City;
