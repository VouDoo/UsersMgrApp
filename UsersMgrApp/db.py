#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# All libs are part of standard distribution for python 3
from configparser import ConfigParser
from datetime import datetime
import re
# SQLAlchemy libs
from sqlalchemy import Column, create_engine, ForeignKey
from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
# Appllication libs
from passwd import *

Base = declarative_base()
dbsession = scoped_session(sessionmaker())


def init_db():
    """
    Initialize database components
    """
    parser = ConfigParser()
    parser.read("config.ini")
    dbfilename = parser.get('database', 'filename')
    engine = create_engine("sqlite:///{}".format(dbfilename), echo=False)
    dbsession.configure(bind=engine, autoflush=False, expire_on_commit=False)
    Base.metadata.create_all(engine)


def get_depts(filter_dept_name=None):
    """
    Get departments from database (can be filtered by department name)

    :param filter_dept_name:
    :return:
    """
    depts_list = list()
    if filter_dept_name:
        result = dbsession.query(Department).filter_by(
            dept_name=filter_dept_name).order_by(
            Department.dept_name)
    else:
        result = dbsession.query(Department).order_by(Department.dept_name)
    for dept in result:
        dept_dict = dict()
        dept_dict["dept_name"] = dept.dept_name
        depts_list.append(dept_dict)
    return depts_list


def add_dept(dept_name, rejected_depts=None):
    """
    Insert department in database

    :param dept_name:
    :param rejected_depts:
    :return:
    """
    depts_list = get_depts(dept_name)
    if depts_list:
        result_msg = "Department {} already exists".format(dept_name)
        return False, result_msg
    if rejected_depts and dept_name in rejected_depts:
        result_msg = "Department {} rejected".format(dept_name)
        return False, result_msg
    else:
        dept = Department()
        dept.dept_name = dept_name
        dbsession.add(dept)
        result_msg = "Department {} added successfully".format(dept_name)
        return True, result_msg
    result_msg = "Error to add {}".format(dept_name)
    return False, result_msg


def update_dept_name(old_dept_name, new_dept_name):
    """
    Update department name in database

    :param old_dept_name:
    :param new_dept_name:
    :return:
    """
    if dbsession.query(Department).filter_by(
            dept_name=new_dept_name).count() == 0:
        dbsession.query(Department).filter_by(
            dept_name=old_dept_name).update({'dept_name': new_dept_name})
        dbsession.query(User).filter_by(user_dept_name=old_dept_name).update(
            {'user_dept_name': new_dept_name})
        result_msg = "Departement {} renamed to {}".format(
            old_dept_name, new_dept_name)
        return True, result_msg
    else:
        result_msg = "Departement {} already exists".format(new_dept_name)
        return False, result_msg
    result_msg = "Departement {} cannot be renamed".format(old_dept_name)
    return False, result_msg


def delete_dept(dept_name):
    """
    Delete department from database

    :param dept_name:
    """
    dbsession.query(Department).filter_by(dept_name=dept_name).delete()
    dbsession.query(User).filter_by(
        user_dept_name=dept_name).update({'user_dept_name': ''})


def get_logins(filter_login_name=None):
    """
    get logins from database (can be filtered by login name)

    :param filter_login_name:
    :return:
    """
    logins_list = list()
    if filter_login_name:
        result = dbsession.query(Login).filter_by(
            login_name=filter_login_name).order_by(
            Login.login_name)
    else:
        result = dbsession.query(Login).order_by(Login.login_name)
    for login in result:
        login_dict = dict()
        login_dict["login_name"] = login.login_name
        login_dict["login_passwd"] = login.login_passwd
        logins_list.append(login_dict)
    return logins_list


def generate_login_name(first_name, last_name, rejected_logins=None):
    """
    Generate login name

    :param first_name:
    :param last_name:
    :param rejected_logins:
    :return:
    """
    login_prefix = first_name.lower().replace(
        ' ',
        '').replace(
        '-',
        '').replace(
            'é',
            'e').replace(
                'è',
        'e')
    login_suffix = last_name.lower().replace(
        ' ',
        '').replace(
        '-',
        '').replace(
            'é',
            'e').replace(
                'è',
        'e')
    login_name = '{prefix}.{suffix}'.format(
        prefix=login_prefix, suffix=login_suffix)
    index_login = 1
    if rejected_logins:
        if dbsession.query(Login).filter_by(
                login_name=login_name).count() > 0 or login_name in rejected_logins:
            temp_login_name = login_name + str(index_login)
            while dbsession.query(Login).filter_by(
                    login_name=temp_login_name).count() > 0 or temp_login_name in rejected_logins:
                index_login += 1
                temp_login_name = login_name + str(index_login)
            login_name += str(index_login)
    else:
        if dbsession.query(Login).filter_by(login_name=login_name).count() > 0:
            temp_login_name = login_name + str(index_login)
            while dbsession.query(Login).filter_by(
                    login_name=temp_login_name).count() > 0:
                index_login += 1
                temp_login_name = login_name + str(index_login)
            login_name += str(index_login)
    return login_name


def renew_login_passwd(login_name):
    """
    Regenerate login password

    :param login_name:
    :return:
    """
    secure_word = generate_secure_word()
    login_passwd = hash_word(secure_word)
    dbsession.query(Login).filter_by(login_name=login_name).update(
        {'login_passwd': login_passwd})
    return secure_word


def get_users(filter_login_name=None):
    """
    Get users from database (can be filtered by login name)

    :param filter_login_name:
    :return:
    """
    users_list = list()
    if filter_login_name:
        result = dbsession.query(User).filter_by(
            user_login_name=filter_login_name).order_by(
            User.user_login_name)
    else:
        result = dbsession.query(User).order_by(User.user_login_name)
    for user in result:
        user_dict = dict()
        user_dict["login_name"] = user.user_login_name
        user_dict["first_name"] = user.user_first_name
        user_dict["maiden_name"] = user.user_maiden_name
        user_dict["last_name"] = user.user_last_name
        user_dict["birth_date"] = user.user_birth_date
        user_dict["post"] = user.user_post
        user_dict["dept_name"] = user.user_dept_name
        user_dict["email_address"] = user.user_email_address
        user_dict["landline_phone"] = user.user_landline_phone
        user_dict["mobile_phone"] = user.user_mobile_phone
        users_list.append(user_dict)
    return users_list


def add_user(
        first_name,
        maiden_name,
        last_name,
        birth_date,
        post,
        dept_name,
        email_address,
        landline_phone,
        mobile_phone,
        rejected_logins=None):
    # Define login
    """
    Insert user in database

    :param first_name:
    :param maiden_name:
    :param last_name:
    :param birth_date:
    :param post:
    :param dept_name:
    :param email_address:
    :param landline_phone:
    :param mobile_phone:
    :param rejected_logins:
    :return:
    """
    login = Login()
    login_name = generate_login_name(first_name, last_name, rejected_logins)
    login.login_name = login_name
    secure_word = generate_secure_word()
    login.login_passwd = hash_word(secure_word)

    # Define user
    user = User()
    user.user_login_name = login.login_name
    user.user_first_name = first_name
    user.user_maiden_name = maiden_name
    user.user_last_name = last_name
    if birth_date:
        user.user_birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
    else:
        user.user_birth_date = ''
    user.user_post = post
    user.user_dept_name = dept_name
    user.user_email_address = email_address
    user.user_landline_phone = landline_phone
    user.user_mobile_phone = mobile_phone

    # Add login and user in database
    dbsession.add_all([login, user])

    # Return used login and generated password
    return login_name, secure_word


def check_user_values(
        first_name,
        maiden_name,
        last_name,
        birth_date,
        post,
        dept_name,
        email_address,
        landline_phone,
        mobile_phone):
    # First name check
    """
    Check values to insert a user in database

    :param first_name:
    :param maiden_name:
    :param last_name:
    :param birth_date:
    :param post:
    :param dept_name:
    :param email_address:
    :param landline_phone:
    :param mobile_phone:
    :return:
    """
    regex = re.compile(r'^[a-zA-Z\s\-éè]+$')
    if regex.match(first_name) is None:
        return False, str(
            "First name cannot be empty and must contain only letters")

    # Maiden name check
    if maiden_name:
        regex = re.compile(r'^[a-zA-Z\s\-éè]+$')
        if regex.match(maiden_name) is None:
            return False, str("Maiden name must contain only letters")

    # Last name check
    regex = re.compile(r'^[a-zA-Z\s\-éè]+$')
    if regex.match(last_name) is None:
        return False, str(
            "Last name cannot be empty and must contain only letters")

    # Birth date check
    regex = re.compile(
        r'^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$')
    if birth_date:
        if regex.match(birth_date) is None:
            return False, str("Birth date format not respected (yyyy-mm-dd)")

    # Post check
    if post:
        regex = re.compile(r'^[\w\s\'\-éè,]+$')
        if regex.match(post) is None:
            return False, str("Post must contain only letters")

    # Department check
    if dept_name:
        regex = re.compile(r'^[\w\s\'\-éè,]+$')
        if regex.match(dept_name) is None:
            return False, str("Department must contain only letters")

    # Email address check
    if email_address:
        regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if regex.match(email_address) is None:
            return False, str("Email address format not respected")

    # Landline phone check
    if landline_phone:
        regex = re.compile(r'^\d{3}[-.]?\d{3}[-.]?\d{4}$')
        if regex.match(landline_phone) is None:
            return False, str(
                "Landline phone number format not respected (example: 0123456789)")

     # Mobile phone check
    if mobile_phone:
        regex = re.compile(r'^\d{3}[-.]?\d{3}[-.]?\d{4}$')
        if regex.match(mobile_phone) is None:
            return False, str("Mobile phone number format not respected")

    return True, str("User format is correct")


def format_user_values(
        first_name,
        maiden_name,
        last_name,
        birth_date,
        post,
        dept_name,
        email_address,
        landline_phone,
        mobile_phone):
    """
    Format user values

    :param first_name:
    :param maiden_name:
    :param last_name:
    :param birth_date:
    :param post:
    :param dept_name:
    :param email_address:
    :param landline_phone:
    :param mobile_phone:
    :return:
    """
    first_name = str(first_name.title())
    maiden_name = str(maiden_name.title())
    last_name = str(last_name.title())
    birth_date = str(birth_date)
    post = str(post)
    dept_name = str(dept_name)
    email_address = str(email_address.lower())
    landline_phone = str(landline_phone)
    mobile_phone = str(mobile_phone)
    return first_name, maiden_name, last_name, birth_date, post, dept_name, email_address, landline_phone, mobile_phone


def delete_user(login_name):
    """
    Delete user from database

    :param login_name:
    """
    dbsession.query(User).filter_by(user_login_name=login_name).delete()
    dbsession.query(Login).filter_by(login_name=login_name).delete()


def edit_user(
        login_name,
        first_name,
        maiden_name,
        last_name,
        birth_date,
        post,
        dept_name,
        email_address,
        landline_phone,
        mobile_phone):
    """
    Update user from database

    :param login_name:
    :param first_name:
    :param maiden_name:
    :param last_name:
    :param birth_date:
    :param post:
    :param dept_name:
    :param email_address:
    :param landline_phone:
    :param mobile_phone:
    :return:
    """
    old_login_name = login_name
    actual_user = get_users(old_login_name)[0]
    if actual_user["first_name"] == first_name and actual_user["last_name"] == last_name:
        new_login_name = old_login_name
    else:
        new_login_name = generate_login_name(first_name, last_name)
    if birth_date:
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
    dbsession.query(User).filter_by(user_login_name=old_login_name).update(
        {
            'user_login_name': new_login_name,
            'user_first_name': first_name,
            'user_maiden_name': maiden_name,
            'user_last_name': last_name,
            'user_birth_date': birth_date,
            'user_post': post,
            'user_dept_name': dept_name,
            'user_email_address': email_address,
            'user_landline_phone': landline_phone,
            'user_mobile_phone': mobile_phone
        }
    )
    dbsession.query(Login).filter_by(login_name=old_login_name).update(
        {
            'login_name': new_login_name
        }
    )
    return new_login_name


class Department(Base):
    __tablename__ = 'department'

    dept_name = Column(String, primary_key=True)

    def __repr__(self):
        """
        Simple representation of rows in table

        :return:
        """
        return "<Department(name='{dept_name}')>".format(dept_name=dept_name)


class Login(Base):
    __tablename__ = 'login'

    login_name = Column(String, primary_key=True)
    login_passwd = Column(String)

    def __repr__(self):
        """
        Simple representation of rows in table

        :return:
        """
        return "<Login(name='{login_name}', passwd='{login_passwd}')>".format(
            login_name=login_name,
            login_passwd=login_passwd)


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'sqlite_autoincrement': True}

    user_id = Column(Integer, primary_key=True)
    user_login_name = Column(
        String,
        ForeignKey(
            Login.login_name),
        nullable=False)
    user_first_name = Column(String, nullable=False)
    user_maiden_name = Column(String)
    user_last_name = Column(String, nullable=False)
    user_birth_date = Column(String)
    user_post = Column(String)
    user_dept_name = Column(Integer, ForeignKey(Department.dept_name))
    user_email_address = Column(String)
    user_landline_phone = Column(String)
    user_mobile_phone = Column(String)
