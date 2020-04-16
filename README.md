# README

	use python program access m3db query url
	use to get m3db namesapce metric and tag information ,  save infomation into  mysql db or localfile 

# mysql DB structure

## db create

	create database m3metric;
	use m3metric;

## table create 
### m3db_namespace

	create table IF NOT EXISTS m3db_namespace (
	  id int not null auto_increment primary key,
	  name varchar(25) not null unique,
	  comment varchar(255)
	) DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

### m3db_metric

	create table IF NOT EXISTS m3db_metric (
	  id int not null auto_increment  primary key,
	  name varchar(100) not null,
	  namespace_id int not null,
	  comment varchar(255),
	  UNIQUE KEY name (name, namespace_id),
	  foreign key(namespace_id) references m3db_namespace(id)
	) DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

### m3db_tag

	create table IF NOT Exists m3db_tag (
	  id int not null auto_increment primary key,
	  name varchar(100) not null,
	  namespace_id int not null,
	  comment varchar(255),
	  UNIQUE KEY name (name, namespace_id),
	  foreign key(namespace_id) references m3db_namespace(id)
	) DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

### m3db_tag_mapping

	create table IF NOT Exists m3db_tag_mapping (
	  metric_id int,
	  tag_id int,
	  foreign key(metric_id) references m3db_metric(id),
	  foreign key(tag_id) references m3db_tag(id)
	);

### namespace insert test

	insert into m3metric.m3db_namespace ( name ) values ( 'app' ), ('app1s'), ('dev');


## SQL select example:

	select a.name, b.name, c.name 
	from  m3db_namespace a, m3db_metric b, m3db_tag c, m3db_tag_mapping d 
	where a.id = b.namespace_id and b.id = d.metric_id and  c.id = d.tag_id and a.name = 'app' and b.name = 'cpu_usage_user';

	+------+----------------+---------------------+
	| name | name           | name                |
	+------+----------------+---------------------+
	| app  | cpu_usage_user | arch                |
	| app  | cpu_usage_user | datacenter          |
	| app  | cpu_usage_user | hostname            |
	| app  | cpu_usage_user | os                  |
	| app  | cpu_usage_user | rack                |
	| app  | cpu_usage_user | region              |
	| app  | cpu_usage_user | service             |
	| app  | cpu_usage_user | service_environment |
	| app  | cpu_usage_user | service_version     |
	| app  | cpu_usage_user | team                |
	+------+----------------+---------------------+
	10 rows in set (0.00 sec)




