
/* Union: basically to combine columns from 2 tables */
/* ex: grab City from Customers and Suppliers tables,
then order the City by the City */

SELECT City FROM Customers
Union
SELECT City FROM Suppliers
order by City;



/* Logic Statement
CASE
  WHEN XXX THEN XXX
  WHEN XXX THEN XXX
  ELSE XXX
END;
*/
SELECT Name, StandardCosts, "Price Comment" =
  CASE
    when StandardCost > 1000 then 'Too Expensive'
    else 'Just Right'
  END
from SalesLT.Product








/*     */
