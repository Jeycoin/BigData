import getpass
from student_management_system import *



def runsystem():
    while True:
        # 提示用户输入指令
        print("\n==========")
        print("Available actions:")
        print("1. Login")
        print("2. Exit")
        action = input("Please enter the action number: ")
        # 退出程序
        if action == "2":
            print("Exiting the program...")
            break
        # 登录
        if action == "1":
            # 提示用户输入用户名和密码
            user_id = input("Enter your user ID: ")
            password = input("Enter your password: ")
            user_type = input("Enter your user type (student, teacher, admin): ")
            #示例登录
            user_type = login(user_id, password, user_type)

            if user_type == 'student':
                student_menu(user_id)
            elif user_type == 'teacher':
                teacher_menu(user_id)
            elif user_type == 'admin':
                admin_menu()
            else:
                print('invalid user_id or password')
def student_menu(user_id,user_type = 'student'):
    while True:
        print("""
        ************* 学生菜单 *************
        1. 查询个人信息
        2. 查询选课信息
        3. 选课
        4. 退课
        5. 查询成绩
        6. 查询班级排名
        7. 修改个人信息
        8. 返回上一级菜单
        *************************************
        """)
        choice = input("请选择操作：")
        if choice == '1':
            query_student_info(user_id,user_type)
            input("Press 1 to go back to the main menu: ")
        elif choice == '2':
            student_query_selection(user_id)
            input("Press 1 to go back to the main menu: ")
        elif choice == '3':
            course_id = input("Enter your select course_id: ")
            student_update_course(user_id,course_id)
            input("Press 1 to go back to the main menu: ")
        elif choice == '4':
            course_id = input("请输入要退选的课程ID：")
            student_update_course(user_id, course_id,select = 'delete')
            input("Press 1 to go back to the main menu: ")
        elif choice == '5':
            student_query_grade(user_id)
        elif choice == '6':
            course_id = input("请输入要查询排名的课程ID：")
            student_query_grade_rank(user_id,course_id)
            input("Press 1 to go back to the main menu: ")
        elif choice == '7':
            select = input("选择修改的信息: ")
            newinfo = input('输入新的{selct}: ')
            update_student_info(user_id,user_type,user_id,select,newinfo)
            input("Press 1 to go back to the main menu: ")
        elif choice == '8':
            break
        else:
            print("无效的选项，请重试！")
def teacher_menu(user_id):
    while True:
        print("""
        ************* 教师菜单 *************
        1. 查询个人信息
        2. 查询课程信息
        3. 查询学生信息
        4. 查询学生成绩单
        5. 查询班级排名
        6. 修改学生成绩
        7. 修改个人信息
        8. 返回上一级菜单
        *************************************
        """)
        choice = input("请选择操作：")
        if choice == '1':
            query_teacher_info(user_id)
            input("Press 1 to go back to the main menu: ")
        elif choice == '2':
            teacher_query_course(user_id)
            input("Press 1 to go back to the main menu: ")
        elif choice == '3':
            student_id = input("输入要查询的学生id（输入0查询所有学生信息）")
            if student_id == '0':
                query_student_info(user_id,'teacher')
            else:
                query_student_info(user_id, 'teacher',student_id)
            input("Press 1 to go back to the main menu: ")
        elif choice == '4':
            course_id = input("输入你要查询的课程成绩：")
            teacher_query_grade(user_id,course_id)
            input("Press 1 to go back to the main menu: ")
        elif choice == '5':
            course_id = input("输入你要查询的课程班级排名：")
            teacher_query_grade_sheet(user_id,course_id)
            input("Press 1 to go back to the main menu: ")
        elif choice == '6':
            course_id = input("课程编号：")
            student_id = input("学生编号：")
            new_grade = input("输入学生该课程更新后成绩：")
            teacher_update_grade(user_id,course_id,student_id,new_grade)
            input("Press 1 to go back to the main menu: ")
        elif choice == '7':
            select = input("选择修改的信息: ")
            newinfo = input('输入新的{selct}: ')
            update_teacher_info(user_id,select,newinfo)
            input("Press 1 to go back to the main menu: ")
        elif choice == '8':
            break
def admin_menu():
    while True:
        print("""
        ************* 管理员菜单 *************
        1. 查询学生信息
        2. 查询教师信息
        3. 查询课程信息
        4. 查询选课信息
        5. 查询成绩信息
        6. 添加学生信息
        7. 添加教师信息
        8. 添加课程信息
        9. 修改学生信息
        10. 修改老师信息
        11. 返回上一级菜单
        *************************************
        """)
        choice = input("请选择操作：")
        if choice == '1':
            student_id = input("输入要查询的学生id（输入0查询所有学生信息）")
            if student_id == '0':
                query_student_info('1','admin')
            else:
                query_student_info('1',user_type='admin',target_student_id=student_id)
            input("Press 1 to go back to the main menu: ")
        elif choice == '2':
            select_table('teacher')
            input("Press 1 to go back to the main menu: ")
        elif choice == '3':
            select_table('course')
            input("Press 1 to go back to the main menu: ")
        elif choice == '4':
            select_table('selection')
            input("Press 1 to go back to the main menu: ")
        elif choice == '5':
            select_table('score')
            input("Press 1 to go back to the main menu: ")
        elif choice == '6':
            id,name,gender,email,phone,password = input("添加的学生id,姓名、性别，邮箱，电话，密码；以空格分隔：").split()
            admin_insert_student(id,name,gender,email,phone,password)
            input("Press 1 to go back to the main menu: ")
        elif choice == '7':
            id, name, gender, email, phone, password = input("添加的老师id,姓名、性别，邮箱，电话，密码；以空格分隔：").split()
            admin_insert_teacher(id, name, gender, email, phone, password)
            input("Press 1 to go back to the main menu: ")
        elif choice == '8':
            id, name, teacher_id = input("添加的课程id、课程名，任课老师id；以空格分隔：").split()
            admin_insert_course(id,name,teacher_id)
            input("Press 1 to go back to the main menu: ")
        elif choice == '9':
            id, name, newinfo = input("指定学生id,修改的列，列值；以空格分隔：").split()
            update_student_info('1',user_type='admin',target_student_id=id,select= name,newinfo = newinfo)
            input("Press 1 to go back to the main menu: ")
        elif choice == '10':
            id, name, newinfo = input("指定学生id,修改的列，列值；以空格分隔：").split()
            update_teacher_info(user_id=id,select=name,newinfo = newinfo)
            input("Press 1 to go back to the main menu: ")
        elif choice == '11':
            break

runsystem()
