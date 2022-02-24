------------------SQL--------------------
select ename, sal,
        case when sal >= 4000 then 'OVERPAID'
             when sal <= 2000 then 'UNDERPAID'
             else 'OK'
        end as status
from emp
------------------------------------
select top 5 * 
from emp
------------------------------------
select top 5 ename,job
from emp
order by newid()
------------------------------------
select * 
from emp
where comm is null
-------------------------------------
select coalesce(comm,0)
from emp
--------------------------------------
select 
    case 
    when comm is not null then comm
    else 0
    end
from emp
-------------------------------------
select ename, job 
from emp
where deptno in (10,20)
and (ename like '%I%' or job like '%ER')
-------------------------------------
select ename, job, sal
from emp 
where deptno = 10
order by sal asc ---order by 3 asc
-------------------------------------
select empno, deptno, sal, ename, job
from emp
order by deptno asc, sal desc
-------------------------------------
select ename, job 
from emp
order by substring (job, lenght(job)-1,2)
---------------------------------------
select ename, sal, comm
from(
select ename, sal,comm,
        case when comm is null then 0 else 1
        end as is_null
        from emp
        )x
order by is_null desc, comm asc
---------------------------------------
select ename, sal, job, comm
from emp
order by case when job = 'SALESMAN' then comm
              else sal
end
--------------Chapter 3-----------------------
select ename as ename_and_dname, deptno
from emp 
where deptno = 10
union all 
select '-------------', null
from t1
union all
select dname, deptno
from dept
-------------JOIN LOGIC IN FROM --------------
select e.ename, d.loc 
from emp e inner join dept d
on (e.deptno = d.deptno)
where e.deptno = 10
------------JOIN LOGIC IN WHERE-----------------
select e.ename, d.loc 
from emp e, dep d 
where e.deptno = d.deptno and e.deptno = 10
-----------------------------------------------
select e.empno, e.ename, e.job, e.sal, e.deptno
from emp e inner join V
on(e.ename = V.ename
e.job = V.job
e.sal = V.sal)
----------EXCEPT IS DIFFERENCE--------------
select deptno from dept
except 
select deptno from emp
-------------------------------------------
select d.*
from dept d left outer join emp e
on (d.deptno = e.deptno)
where e.deptno is null
-----------------------------------------
select e.ename, d.loc, eb.recieved
from emp e join dept d
on (e.deptno = d.deptno)
left join emp_bonus eb 
on (e.empno = eb.empno)
order by 2
--OR ------------------------
select e.ename, d.loc
   select(eb.recieved from emp_bonus eb
        where eb.empno = e.empno) as recieved 
from emp e, dept d 
where e.deptno = d.deptno
order by 2  
-----------------3.7-------------------------
---------------------------------------------
select ename ,commfrom emp
where coalesce(comm,0)<(select comm from emp where ename = 'WARD')
---------------------------------------------
insert into dept (deptno, dname, loc)
values (50, 'programming', 'baltimore')
-------------------------------------------
insert into dept_east (deptno, dname, loc)
select (deptno, dname, loc)
from dept
where loc in ( 'new york', 'boston')
---------------------------------------------
select *
into dept_2
from dept
where 1 = 0
-----------------------------------------
update emp 
set sal = sal * 1.1
where deptno = 20
--OR
select deptno, ename,
        sal as orig_sal
        sal * 0.1 as amt_added
        sal * 1.1 as new_sal
from emp
where deptno = 20
order by 1,5
---------------------------------------------
update emp
set sal = sal * 1.2
where empno in (select empno from emp_bonus)
----------------------------------------------
update emp e, new_sal ns 
set e.sal = ns.sal
set e.comm = ns.sal/2 
where e.deptno = ns.deptno
------------------------------------------------
merge into emp_commission ec --table to be updated 
using (select * from emp)emp -- sub query named emp to be compared with
on (ec.deptno = emp.deptno) -- join
when matched then
        update set ec.comm = 1000
        delete where (sal < 2000)
when not matched then
        insert into (ec.empno, ec.ename, ec.deptno, ec.comm)
        values (emp.empno, emp.ename, emp.deptno, emp.com)
--------------------------------------------------------------
delete from emp 
where 
--OR if you want to delete all records
truncate table emp 
-------------------------------------------------------------
delete from emp
where not exist 
        (select * from dept
        where dept.deptno = emp.deptno)
----------------------------------------------------------
delete from dupes       --group by name will return name, if there is same name with more than
where id not in (       --id, query will select the min id and then delete the other ids for this name
        select min(id) from dupes
        group by name)
------------------------------------------------------
delete from emp
where deptno in (select deptno from dept_accidents
                        group by deptno
                        having count(*) >= 3)
------------CHAPTER 5 META DATA QUERIES-----------------------
select table_name
from information_schema.tables
where table_schema = 'SMAEGOL'
-----------------------------------------------
 select column_name
 from information_schema.columns
 where table_schema = 'SMEAGOL'
 and table_name = 'EMP'
 ---------------------------------------------

