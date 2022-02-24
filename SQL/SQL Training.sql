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



