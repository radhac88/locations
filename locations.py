from settings import *
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

import json

db = SQLAlchemy(app)


class Location(db.Model):
    __tablename__ = 'location' 
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(50), nullable=True)


    def json(self):
        return {'id': self.id, 'name': self.name,
                'description': self.description}

    def add_location(_name, _description):
        new_location = Location(name=_name, description=_description)
        db.session.add(new_location)  # add new location to database session
        db.session.commit()  # commit changes to session

    def get_all_locations():
        recs_lit= Location.query.all()
        print(recs_lit)
        return [Location.json(location) for location in recs_lit]

    def get_location(_id):
        return [Location.json(Location.query.filter_by(id=_id).first())]

    def update_location(_id, _name, _description):
        location_to_update = Location.query.filter_by(id=_id).first()
        location_to_update.name = _name
        location_to_update.description = _description
        db.session.commit()

    def delete_location(_id):
        Location.query.filter_by(id=_id).delete()
        db.session.commit()


class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(50), nullable=True)


    def json(self):
        return {'id': self.id, 'name': self.name,
                'description': self.description}

    def add_department(_name, _description):
        new_department = Department(name=_name, description=_description)
        db.session.add(new_department)  # add new department to database session
        db.session.commit()  # commit changes to session

    def get_all_departments():
        return [Department.json(department) for department in Department.query.all()]

    '''Can reuse for all the classes '''
    def get_matched_departments(depids_list,clsname):
        return [clsname.json(depobj) for depobj in clsname.query.filter(clsname.id.in_(depids_list)).all()]

    def get_department(_id):
        return [Department.json(Department.query.filter_by(id=_id).first())]

    def get_category_by_dept_and_loc_id(_locid, _depid):
        deprecs = db.session.query(Metadata.category_id).filter(and_(Metadata.location_id == _locid, Metadata.department_id == _depid)).distinct().all()
        dep_list = list(list(zip(*deprecs))[0])
        print(_locid, _depid)
        print(dep_list)
        dep_recs = Department.get_matched_departments(dep_list, Category)
        return dep_recs


    def get_department_by_loc(_id):
        deprecs = db.session.query(Metadata.department_id).filter(Metadata.location_id==_id).distinct().all()
        dep_list=list(list(zip(*deprecs))[0])
        dep_recs = Department.get_matched_departments(dep_list, Department)
        return dep_recs

    def update_department(_id, _name, _description):
        department_to_update = Department.query.filter_by(id=_id).first()
        department_to_update.name = _name
        department_to_update.description = _description
        db.session.commit()

    def delete_department(_id):
        Department.query.filter_by(id=_id).delete()
        db.session.commit()

class Category(db.Model):
    __tablename__ = 'category' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(50), nullable=True)


    def json(self):
        return {'id': self.id, 'name': self.name,
                'description': self.description}

    def add_category(_name, _description):
        new_category = Category(name=_name, description=_description)
        db.session.add(new_category)  # add new category to database session
        db.session.commit()  # commit changes to session

    def get_all_categorys():
        return [Category.json(category) for category in Category.query.all()]

    def get_category(_id):
        return [Category.json(Category.query.filter_by(id=_id).first())]

    def update_category(_id, _name, _description):
        category_to_update = Category.query.filter_by(id=_id).first()
        category_to_update.name = _name
        category_to_update.description = _description
        db.session.commit()

    def delete_category(_id):
        Category.query.filter_by(id=_id).delete()
        db.session.commit()

class SubCategory(db.Model):
    __tablename__ = 'subcategory' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(50), nullable=True)


    def json(self):
        return {'id': self.id, 'name': self.name,
                'description': self.description}

    def add_subcategory(_name, _description):
        new_subcategory = SubCategory(name=_name, description=_description)
        db.session.add(new_subcategory)  # add new subcategory to database session
        db.session.commit()  # commit changes to session

    def get_all_subcategorys():
        return [SubCategory.json(subcategory) for subcategory in SubCategory.query.all()]

    def get_subcategory(_id):
        return [SubCategory.json(SubCategory.query.filter_by(id=_id).first())]

    def update_subcategory(_id, _name, _description):
        subcategory_to_update = SubCategory.query.filter_by(id=_id).first()
        subcategory_to_update.name = _name
        subcategory_to_update.description = _description
        db.session.commit()

    def delete_subcategory(_id):
        SubCategory.query.filter_by(id=_id).delete()
        db.session.commit()

class Metadata(db.Model):
    __tablename__ = 'metadata' 
    id = db.Column(db.Integer, primary_key=True) 
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    sub_category_id = db.Column(db.Integer, db.ForeignKey("subcategory.id"))


    location_info = relationship("Location")
    department_info = relationship("Department")
    category_info = relationship("Category")
    sub_category_info = relationship("SubCategory")

    @hybrid_property
    def location_name(self):
        return self.location_info.name

    @hybrid_property
    def department_name(self):
        return self.department_info.name

    @hybrid_property
    def category_name(self):
        return self.category_info.name

    @hybrid_property
    def subcategory_name(self):
        return self.sub_category_info.name

    def json(self):
        return {"location": self.location_name, "department": self.department_name,
                "category": self.category_name, "subcategory": self.subcategory_name}

    def get_metadata(_id=None):
        if _id is None:
            return [Metadata.json(meta) for meta in Metadata.query.all()]
        result = Metadata.query.filter_by(id=_id).first()
        if result:
            return Metadata.json(result)
        else:
            return "Record Not found"

    def update_metadata(_id, _name, _description):
        subcategory_to_update = SubCategory.query.filter_by(id=_id).first()
        subcategory_to_update.name = _name
        subcategory_to_update.description = _description
        db.session.commit()

    def delete_metadata(_id):
        SubCategory.query.filter_by(id=_id).delete()
        db.session.commit()

#db.create_all()
