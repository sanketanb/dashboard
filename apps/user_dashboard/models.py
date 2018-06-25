from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
NAME_REGEX = re.compile(r'[a-zA-Z]+')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
class UserManager(models.Manager):
    def validate(self, post_data):
        errors = []
        p = post_data
        first_name, last_name, email, password, cpassword = p['first_name'], p['last_name'], p['email'], p['password'], p['cpassword']
        
        if not first_name or not last_name or not email or not password or not cpassword:
            errors.append("All fields are required")
        else:
            if len(first_name) < 2 or len(last_name) < 2 or not re.match(NAME_REGEX, first_name) or not re.match(NAME_REGEX, last_name):
                errors.append("Invalid names")            
            if not re.match(EMAIL_REGEX, email):
                errors.append("Invalid email") 
            if len(password) <8:
                errors.append("Invalid password!")
            elif password != cpassword:
                errors.append("Passwords must match")
        
        if not errors:
            if self.filter(email=email):
                errors.append("email already in use")
            else:     
                hash_in = bcrypt.hashpw(password.encode(), bcrypt.gensalt())                
                if self.count() == 0:
                    return self.create(
                        firstname = first_name,
                        lastname = last_name,
                        email = email,
                        password = hash_in,
                        user_level = 9
                    )    
                else: 
                    return self.create(
                        firstname = first_name,
                        lastname = last_name,
                        email = email,
                        password = hash_in,
                        user_level = 1
                    )    
        return errors
    def validate_signin(self, signin_data):
        errors = []
        email, password = signin_data['email'], signin_data['password']
        if not email or not password:
            errors.append("All fields are required")
        else:
            if not re.match(EMAIL_REGEX, email) or len(password) <8:
                errors.append("Invalid fields") 
            #  existing email check
            else:
                persons = self.filter(email=email)
                if len(persons) == 0:
                    errors.append("Please register")
                else:
                    hash1 = persons[0].password
                    if bcrypt.checkpw(password.encode(), hash1.encode()) == True:
                        # print ("password match")
                        # taking only the first user from the filtered persons, index=0
                        user = persons[0]
                        return user
                    else:
                        errors.append("Invalid password")
        return errors
    def validate_user_info(self, info_data, user_id):
        errors = []        
        if len(info_data['first_name']) < 2:
            errors.append("User first name should be more than 2 characters")
        if len(info_data['last_name']) < 2:
            errors.append("User last name should be more than 2 characters")
        
        check = self.get(id=user_id)
        if check.email != info_data['email']:
            print('inside first if')
            if not re.match(EMAIL_REGEX, info_data['email']):
                errors.append("invalid email") 
            #  existing email check
            else:
                users = self.filter(email = info_data['email'].lower())
                if users:
                    errors.append("email already in use")
        if not errors:
            print('inside second if')
            try:
                check.firstname = info_data['first_name']
                check.lastname = info_data['last_name']
                check.email = info_data['email'].lower()
                check.save()
                return check
            except:
                pass
        return errors
    def validate_user_pwd(self, pwd_data, user_id):
        errors=[]
        password, cpassword = pwd_data['password'], pwd_data['cpassword']
        if not password or not cpassword:
            errors.append("Both fields are required")
        else:
            if len(password) < 8:
                errors.append("invalid password")
            elif password != cpassword:
                errors.append("passwords must match")
        
        if not errors:
            hash_in = bcrypt.hashpw(password.encode(), bcrypt.gensalt())   
            check = self.get(id=user_id)             
            check.password = hash_in
            check.save()
            return check
        return errors

class MessageManager(models.Manager):
    # this class has utility method to retrive messages + comment for user's wall display
    def retrieve_comments_with_msg(self, wall_user):
        # wall_user is individual user object
        message_models = []     
        # initializing empty array   
        messages=self.filter(receiver=wall_user).order_by("-created_at")
        for message in messages:
            # MessageModel is grouping my objects in a particular way
            message_models.append(MessageModel(message,message.comments.all()))
        return message_models
    
class MessageModel:
    def __init__(self,message,comments):
        # this init is my constructor 
        self.message = message
        self.comments = comments

class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_level = models.IntegerField()
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    # def __str__(self):
    #     return "<User object: {} {} {}>".format(self.firstname, self.lastname, self.email, self.password)
class Message(models.Model):
    desc = models.TextField()
    # one user can write many messages
    author = models.ForeignKey(User, related_name="written_messages")
    # one user can receive many messages
    receiver = models.ForeignKey(User, related_name="received_messages")
    created_at = models.DateTimeField(auto_now_add = True)
    objects = MessageManager()

class Comment(models.Model):
    desc = models.TextField()
    # one comment has one author, one user has many comments
    author = models.ForeignKey(User, related_name="comments")
    # one comment belongs to one message, one message has many comments
    message = models.ForeignKey(Message, related_name="comments")
    created_at = models.DateTimeField(auto_now_add = True)
    


