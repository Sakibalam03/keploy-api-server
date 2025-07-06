#include <gtest/gtest.h>
#include "Department.h"
#include "Job.h"
#include "Person.h"
#include "User.h"
#include "PersonInfo.h"
#include "Jwt.h"

TEST(DepartmentTest, ConstructorAndGetters) {
    drogon::orm::Row row;
    row.push_back(1);
    row.push_back("Sales");
    drogon_model::org_chart::Department dept(row);
    EXPECT_EQ(dept.getValueOfId(), 1);
    EXPECT_EQ(dept.getValueOfName(), "Sales");
}

TEST(DepartmentTest, EmptyConstructor) {
    drogon_model::org_chart::Department dept;
    EXPECT_EQ(dept.getId(), nullptr);
    EXPECT_EQ(dept.getName(), nullptr);
}

TEST(DepartmentTest, JsonConstructor) {
    Json::Value json;
    json["id"] = 1;
    json["name"] = "Sales";
    drogon_model::org_chart::Department dept(json);
    EXPECT_EQ(dept.getValueOfId(), 1);
    EXPECT_EQ(dept.getValueOfName(), "Sales");
}

TEST(DepartmentTest, Setters) {
    drogon_model::org_chart::Department dept;
    dept.setId(1);
    dept.setName("Marketing");
    EXPECT_EQ(dept.getValueOfId(), 1);
    EXPECT_EQ(dept.getValueOfName(), "Marketing");
}


TEST(JobTest, ConstructorAndGetters) {
    drogon::orm::Row row;
    row.push_back(1);
    row.push_back("Software Engineer");
    drogon_model::org_chart::Job job(row);
    EXPECT_EQ(job.getValueOfId(), 1);
    EXPECT_EQ(job.getValueOfTitle(), "Software Engineer");
}

TEST(JobTest, EmptyConstructor) {
    drogon_model::org_chart::Job job;
    EXPECT_EQ(job.getId(), nullptr);
    EXPECT_EQ(job.getTitle(), nullptr);
}

TEST(JobTest, JsonConstructor) {
    Json::Value json;
    json["id"] = 1;
    json["title"] = "Software Engineer";
    drogon_model::org_chart::Job job(json);
    EXPECT_EQ(job.getValueOfId(), 1);
    EXPECT_EQ(job.getValueOfTitle(), "Software Engineer");
}

TEST(JobTest, Setters) {
    drogon_model::org_chart::Job job;
    job.setId(2);
    job.setTitle("Data Scientist");
    EXPECT_EQ(job.getValueOfId(), 2);
    EXPECT_EQ(job.getValueOfTitle(), "Data Scientist");
}


TEST(PersonTest, ConstructorAndGetters) {
    drogon::orm::Row row;
    row.push_back(1);
    row.push_back(1);
    row.push_back(1);
    row.push_back(nullptr);
    row.push_back("John");
    row.push_back("Doe");
    row.push_back(trantor::Date(2023,10,27));
    drogon_model::org_chart::Person person(row);
    EXPECT_EQ(person.getValueOfId(), 1);
    EXPECT_EQ(person.getValueOfJobId(), 1);
    EXPECT_EQ(person.getValueOfDepartmentId(), 1);
    EXPECT_EQ(person.getValueOfFirstName(), "John");
    EXPECT_EQ(person.getValueOfLastName(), "Doe");
    EXPECT_EQ(person.getValueOfHireDate().year(), 2023);
    EXPECT_EQ(person.getValueOfHireDate().month(), 10);
    EXPECT_EQ(person.getValueOfHireDate().day(), 27);
}

TEST(PersonTest, EmptyConstructor) {
    drogon_model::org_chart::Person person;
    EXPECT_EQ(person.getId(), nullptr);
    EXPECT_EQ(person.getJobId(), nullptr);
    EXPECT_EQ(person.getDepartmentId(), nullptr);
    EXPECT_EQ(person.getFirstName(), nullptr);
    EXPECT_EQ(person.getLastName(), nullptr);
    EXPECT_EQ(person.getHireDate(), nullptr);
}

TEST(PersonTest, Setters) {
    drogon_model::org_chart::Person person;
    person.setId(2);
    person.setJobId(2);
    person.setDepartmentId(2);
    person.setFirstName("Jane");
    person.setLastName("Smith");
    person.setHireDate(trantor::Date(2024, 1, 15));
    EXPECT_EQ(person.getValueOfId(), 2);
    EXPECT_EQ(person.getValueOfJobId(), 2);
    EXPECT_EQ(person.getValueOfDepartmentId(), 2);
    EXPECT_EQ(person.getValueOfFirstName(), "Jane");
    EXPECT_EQ(person.getValueOfLastName(), "Smith");
    EXPECT_EQ(person.getValueOfHireDate().year(), 2024);
    EXPECT_EQ(person.getValueOfHireDate().month(), 1);
    EXPECT_EQ(person.getValueOfHireDate().day(), 15);
}


TEST(UserTest, ConstructorAndGetters) {
    drogon::orm::Row row;
    row.push_back(1);
    row.push_back("john.doe");
    row.push_back("password123");
    drogon_model::org_chart::User user(row);
    EXPECT_EQ(user.getValueOfId(), 1);
    EXPECT_EQ(user.getValueOfUsername(), "john.doe");
    EXPECT_EQ(user.getValueOfPassword(), "password123");
}

TEST(UserTest, EmptyConstructor) {
    drogon_model::org_chart::User user;
    EXPECT_EQ(user.getId(), nullptr);
    EXPECT_EQ(user.getUsername(), nullptr);
    EXPECT_EQ(user.getPassword(), nullptr);
}

TEST(UserTest, Setters) {
    drogon_model::org_chart::User user;
    user.setId(2);
    user.setUsername("jane.smith");
    user.setPassword("securepass");
    EXPECT_EQ(user.getValueOfId(), 2);
    EXPECT_EQ(user.getValueOfUsername(), "jane.smith");
    EXPECT_EQ(user.getValueOfPassword(), "securepass");
}


TEST(PersonInfoTest, ConstructorAndGetters) {
    drogon::orm::Row row;
    row.push_back(1);
    row.push_back(1);
    row.push_back("Software Engineer");
    row.push_back(1);
    row.push_back("Sales");
    row.push_back(nullptr);
    row.push_back(nullptr);
    row.push_back("John");
    row.push_back("Doe");
    row.push_back(trantor::Date(2023,10,27));
    drogon_model::org_chart::PersonInfo personInfo(row);
    EXPECT_EQ(personInfo.getValueOfId(), 1);
    EXPECT_EQ(personInfo.getValueOfJobId(), 1);
    EXPECT_EQ(personInfo.getValueOfJobTitle(), "Software Engineer");
    EXPECT_EQ(personInfo.getValueOfFirstName(), "John");
    EXPECT_EQ(personInfo.getValueOfLastName(), "Doe");
    EXPECT_EQ(personInfo.getValueOfHireDate().year(), 2023);
    EXPECT_EQ(personInfo.getValueOfHireDate().month(), 10);
    EXPECT_EQ(personInfo.getValueOfHireDate().day(), 27);
}

TEST(PersonInfoTest, EmptyConstructor) {
  drogon_model::org_chart::PersonInfo personInfo;
  EXPECT_EQ(personInfo.getId(), nullptr);
  EXPECT_EQ(personInfo.getJobId(), nullptr);
  EXPECT_EQ(personInfo.getJobTitle(), nullptr);
  EXPECT_EQ(personInfo.getFirstName(), nullptr);
  EXPECT_EQ(personInfo.getLastName(), nullptr);
  EXPECT_EQ(personInfo.getHireDate(), nullptr);
}



TEST(JwtTest, EncodeDecode) {
    Jwt jwt("secret", 3600, "issuer");
    std::string token = jwt.encode("userId", 123);
    auto decoded = jwt.decode(token);
    EXPECT_EQ(decoded.get_payload()["userId"].get<int>(), 123);
}

TEST(JwtTest, EmptyTokenDecode) {
  Jwt jwt("secret", 3600, "issuer");
  auto decoded = jwt.decode("");
  EXPECT_TRUE(decoded.get_payload().empty());
}

TEST(JwtTest, InvalidTokenDecode) {
  Jwt jwt("secret", 3600, "issuer");
  auto decoded = jwt.decode("invalidtoken");
  EXPECT_TRUE(decoded.get_payload().empty());
}