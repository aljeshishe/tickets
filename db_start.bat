docker run -e MYSQL_ROOT_PASSWORD=root -p 33306:3306 -v %cd%\db:/var/lib/mysql -it mysql:8 
