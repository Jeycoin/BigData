from pymysql import Error
import pymysql
# 连接数据库
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123123',
    'database': 'student_management'
}
def create_conn():
    try:
        conn = pymysql.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None
def create_tables():
    conn = create_conn()
    if conn is None:
        return

    cursor = conn.cursor()

    create_student_table = '''
    CREATE TABLE IF NOT EXISTS student (
        student_id VARCHAR(10) NOT NULL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        gender VARCHAR(10) NOT NULL,
        email VARCHAR(50) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        password VARCHAR(20) NOT NULL
    );
    '''
    cursor.execute(create_student_table)

    # 创建教师表格
    create_teacher_table = '''
    CREATE TABLE IF NOT EXISTS teacher (
        teacher_id VARCHAR(10) NOT NULL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        gender VARCHAR(10) NOT NULL,
        email VARCHAR(50) NOT NULL,
        password VARCHAR(20) NOT NULL
    );
    '''
    cursor.execute(create_teacher_table)

    # 创建课程表格
    create_course_table = '''
    CREATE TABLE IF NOT EXISTS course (
        course_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        teacher_id VARCHAR(10) NOT NULL,
        FOREIGN KEY (teacher_id) REFERENCES teacher(teacher_id)
    );
    '''
    cursor.execute(create_course_table)

    # 创建选课表格
    create_selection_table = '''
    CREATE TABLE IF NOT EXISTS selection (
        student_id VARCHAR(10) NOT NULL,
        course_id INT NOT NULL,
        PRIMARY KEY (student_id, course_id),
        FOREIGN KEY (student_id) REFERENCES student(student_id),
        FOREIGN KEY (course_id) REFERENCES course(course_id)
    );
    '''
    cursor.execute(create_selection_table)

    # 创建成绩表格
    create_score_table = '''
    CREATE TABLE IF NOT EXISTS score (
        student_id VARCHAR(10) NOT NULL,
        course_id INT NOT NULL,
        score FLOAT DEFAULT NULL,
        PRIMARY KEY (student_id, course_id),
        FOREIGN KEY (student_id) REFERENCES student(student_id),
        FOREIGN KEY (course_id) REFERENCES course(course_id)
    );
    '''
    cursor.execute(create_score_table)

    # 关闭游标对象和数据库连接
    cursor.close()
    conn.close()
def print_all_tables():
    conn = create_conn()
    if not conn:
        return

    cursor = conn.cursor()

    # 获取所有表名
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    # 打印所有表名
    print("Tables in the database:")
    for table in tables:
        print(f"- {table[0]}")

    conn.close()
def init_users():
    # 向学生表中插入用户信息
    conn = create_conn()
    cursor = conn.cursor()
    try:
        admins = [
            ('10001', '123456'),
            ('10002', '123456')
        ]
        insert_admin = '''
        INSERT INTO admin (admin_id, password)
        VALUES (%s, %s)
        '''

        students = [
            ('201901001', '张三', '男', 'zhangsan@example.com', '13812345678', '123456'),
            ('201901002', '李四', '女', 'lisi@example.com', '13912345678', '123456'),
            ('201901003', '王五', '男', 'wangwu@example.com', '13612345678', '123456')
        ]
        insert_student = '''
        INSERT INTO student(student_id, name, gender, email, phone, password) 
        VALUES(%s, %s, %s, %s, %s, %s);
        '''

        # 向教师表中插入用户信息
        teachers = [
            ('1001', '张老师', '男', 'zhanglaoshi@example.com', '123456'),
            ('1002', '李老师', '女', 'lilaoshi@example.com', '123456'),
            ('1003', '王老师', '男', 'wanglaoshi@example.com', '123456')
        ]
        insert_teacher = '''
        INSERT INTO teacher(teacher_id, name, gender, email, password) 
        VALUES(%s, %s, %s, %s, %s);
        '''

        cursor.executemany(insert_admin, admins)
        conn.commit()
        # 插入学生用户信息
        cursor.executemany(insert_student, students)
        conn.commit()

        # 插入教师用户信息
        cursor.executemany(insert_teacher, teachers)
        conn.commit()
    except Error as e:
        print(f"Error: {e}")
    # 关闭游标对象和数据库连接
    cursor.close()
    conn.close()
def select_table(table_name):
    # 创建数据库连接
    conn = create_conn()
    cursor = conn.cursor()

    # 查询指定表格的所有记录
    select_all = f'SELECT * FROM {table_name};'
    cursor.execute(select_all)
    results = cursor.fetchall()

    # 打印查询结果
    for result in results:
        print(result)

    # 关闭游标对象和数据库连接
    cursor.close()
    conn.close()
def login(user_id, password, user_type):
    conn = create_conn()
    if conn is None:
        return None
    cursor = conn.cursor()
    #使用参数绑定的方法防止sql注入
    try:
        if user_type == 'student':
            cursor.execute("""
            SELECT student_id, name FROM student
            WHERE student_id = %s AND password = %s
            """, (user_id, password))
        elif user_type == 'teacher':
            cursor.execute("""
            SELECT teacher_id, name FROM teacher
            WHERE teacher_id = %s AND password = %s
            """, (user_id, password))
        elif user_type == 'admin':
            # 假设管理员信息存储在一个名为admins的表中
            cursor.execute("""
            SELECT admin_id  FROM admin
            WHERE admin_id = %s AND password = %s
            """, (user_id, password))
        else:
            print("Invalid user type.")
            return None

        result = cursor.fetchone()
        if result is not None:
            print(f"Welcome!")
        else:
            return None
            print("Login failed. Invalid user ID or password.")

    except Error as e:
        print(f"Error: {e}")

    cursor.close()
    conn.close()
    return user_type
def query_student_info(user_id, user_type, target_student_id=None):
    conn = create_conn()
    if conn is None:
        return

    cursor = conn.cursor()

    try:
        if user_type == 'student':
            # 学生用户只能查询自己的信息
            cursor.execute("""
            SELECT * FROM student
            WHERE student_id = %s
            """, (user_id,))
        elif user_type == 'teacher':
            if target_student_id:
                # 管理员用户可以查询指定学生信息
                cursor.execute("""
                SELECT * FROM student
                WHERE student_id = %s
                """, (target_student_id,))
            else:
                cursor.execute("SELECT * FROM student")
        elif user_type == 'admin':
            if target_student_id:
                # 管理员用户可以查询指定学生信息
                cursor.execute("""
                SELECT * FROM student
                WHERE student_id = %s
                """, (target_student_id,))
            else:
                # 管理员用户可以查看整张学生表
                cursor.execute("SELECT * FROM student")
        else:
            print("Invalid user type.")
            return

        result = cursor.fetchall()
        for row in result:
            print(row)

    except Error as e:
        print(f"Error: {e}")

    cursor.close()
    conn.close()
def query_teacher_info(user_id, user_type = 'teacher', target_student_id=None):
    conn = create_conn()
    if conn is None:
        return

    cursor = conn.cursor()

    try:
        if user_type == 'teacher':
            # 学生用户只能查询自己的信息
            cursor.execute("""
            SELECT * FROM teacher
            WHERE teacher_id = %s
            """, (user_id,))
        else:
            print("Invalid user type.")
            return

        result = cursor.fetchall()
        for row in result:
            print(row)
    except Error as e:
        print(f"Error: {e}")

    cursor.close()
    conn.close()
def update_student_info(user_id, user_type,target_student_id,select,newinfo):
    if user_type != 'admin' and user_id != target_student_id:
        print("You do not have permission to update this student's information.")
        return

    conn = create_conn()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
        update_sql = f'''
            UPDATE student SET {select}='{newinfo}'
            WHERE student_id='{target_student_id}';
            '''
        cursor.execute(update_sql)
        conn.commit()
        print("Student information updated successfully.")

    except Error as e:
        print(f"Error: {e}")
    cursor.close()
    conn.close()
def update_teacher_info(user_id,select,newinfo):
    conn = create_conn()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
        update_sql = f'''
            UPDATE teacher SET {select}='{newinfo}'
            WHERE student_id='{user_id}';
            '''
        cursor.execute(update_sql)
        conn.commit()
        print("Teacher information updated successfully.")

    except Error as e:
        print(f"Error: {e}")
    cursor.close()
    conn.close()
def student_query_course(course_id=None):
    conn = create_conn()
    if conn is None:
        return
    cursor = conn.cursor()
    # 防止SQL注入
    if course_id is not None:
        course_id = pymysql.escape_string(course_id)

    try:
        # 查询指定课程或所有课程信息
        if course_id is not None:
            select_sql = f'''
            SELECT * FROM course WHERE course_id='{course_id}';
            '''
        else:
            select_sql = '''
            SELECT * FROM course;
            '''
        cursor.execute(select_sql)
        results = cursor.fetchall()

        # 打印查询结果
        for result in results:
            print(result)

    except Error as e:
        print(f"Error: {e}")
    # 关闭游标对象和数据库连接
    cursor.close()
    conn.close()
def teacher_update_course(course_id, teacher_id, new_course_name):
    conn = create_conn()
    if conn is None:
        return
    cursor = conn.cursor()

    # 防止SQL注入
    course_id = pymysql.escape_string(course_id)
    teacher_id = pymysql.escape_string(teacher_id)
    new_course_name = pymysql.escape_string(new_course_name)

    # 修改课程信息
    update_sql = f'''
    UPDATE course SET course_name='{new_course_name}'
    WHERE course_id='{course_id}' AND teacher_id='{teacher_id}';
    '''
    cursor.execute(update_sql)
    conn.commit()

    # 关闭游标对象和数据库连接
    cursor.close()
    conn.close()
def admin_update_course(course_id, course_name, teacher_id,select = 'insert',new_course_name= None):
    conn = create_conn()
    if conn is None:
        return
    cursor = conn.cursor()

    # 插入课程信息
    insert_sql = f'''
            INSERT INTO course(course_id, name, teacher_id) 
            VALUES('{course_id}', '{course_name}', '{teacher_id}');
            '''
    delete_sql = f'''
                DELETE FROM course WHERE course_id='{course_id}';
                '''
    update_sql = f'''
                UPDATE course SET name = '{new_course_name}'
                WHERE course_id='{course_id}' AND teacher_id='{teacher_id}';
                '''
    try:
        if select == 'insert':
            cursor.execute(insert_sql)
        elif select == 'delete':
            cursor.execute(delete_sql)
        elif select == 'update':
            cursor.execute(update_sql)
        else:
            print('None approach')
        conn.commit()
    except Error as e:
        print(f"Error: {e}")
    # 关闭游标对象和数据库连接
    cursor.close()
    conn.close()
def student_update_course(user_id, course_id, select ='insert'):
    conn = create_conn()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
        select_sql = f"SELECT * FROM course WHERE course_id='{course_id}';"
        cursor.execute(select_sql)
        result = cursor.fetchone()
        if not result:
            print("Course not found.")
            return
            # 查询是否已经选过该课程
        if select == 'insert':
            select_sql = f"SELECT * FROM selection WHERE student_id='{user_id}' AND course_id='{course_id}';"
            cursor.execute(select_sql)
            result = cursor.fetchone()
            if result:
                print("You have already selected this course.")
                return

            insert_sql = f'''
            INSERT INTO selection(student_id, course_id) VALUES('{user_id}', '{course_id}');
            '''
            cursor.execute(insert_sql)
            conn.commit()

            insert_grade_sql = f"INSERT INTO score VALUES ('{user_id}', '{course_id}',NULL);"
            cursor.execute(insert_grade_sql)
            conn.commit()
            print("Grade record inserted successfully.")
            print(f"Student {user_id} selected course {course_id} successfully!")

        elif select == 'delete':
            delete_sql = f'''
            DELETE FROM selection WHERE student_id='{user_id}' AND course_id='{course_id}';
            '''
            cursor.execute(delete_sql)
            conn.commit()

            delete_grade_sql = f'''
                    DELETE FROM score WHERE student_id='{user_id}' AND course_id='{course_id}';
                    '''
            cursor.execute(delete_grade_sql)
            conn.commit()
            print(f"Student {user_id} dropped course {course_id} successfully!")

        # 同步更新成绩表

    except Error as e:
        print(f"Error: {e}")
    # 关闭游标对象和数据库连接
    cursor.close()
    conn.close()

    def teacher_update_course(user_id, course_id, new_teacher_id):
        # 防止SQL注入
        conn = create_conn()
        if conn is None:
            return
        cursor = conn.cursor()
        try:
            # 检查操作是否合法
            select_sql = f"SELECT * FROM course WHERE teacher_id='{user_id}' AND course_id='{course_id}';"
            cursor.execute(select_sql)
            result = cursor.fetchone()

            if not result:
                print("You can only modify the course you teach!")
                return
            else:
                # 更新课程信息
                update_sql = f"UPDATE course SET  teacher_id ='{new_teacher_id}' WHERE course_id='{course_id}';"
                cursor.execute(update_sql)
                conn.commit()
                print(f"Updated teacher_id to {new_teacher_id} for course {course_id} successfully!")
        except Error as e:
            print(f"Error: {e}")
        # 关闭游标对象和数据库连接
        cursor.close()
        conn.close()
        # 要制定teacherid为一个teacher表中确切
def student_query_selection(user_id):
    conn = create_conn()
    if conn is None:
        return
    cursor = conn.cursor()

    try:
        # 查询选课信息，包括所选课程的老师、课程名称和课程ID
        select_sql = f'''
        SELECT course.course_id, course.name, teacher.name 
        FROM selection 
        JOIN course ON selection.course_id = course.course_id 
        JOIN teacher ON course.teacher_id = teacher.teacher_id 
        WHERE selection.student_id='{user_id}';
        '''
        cursor.execute(select_sql)
        results = cursor.fetchall()

        # 打印查询结果
        for result in results:
            print(f"Course ID: {result[0]} | Course Name: {result[1]} | Teacher: {result[2]}")

    except Error as e:
        print(f"Error: {e}")
    # 关闭游标对象和数据库连接
    cursor.close()
    conn.close()
def student_query_grade(user_id):
    conn = create_conn()
    if conn is None:
        return
    cursor = conn.cursor()
    # 防止SQL注入
    # user_id = conn.escape_string(user_id)
    # 查询成绩信息
    select_sql = f'''
    SELECT * FROM score WHERE student_id='{user_id}';
    '''
    cursor.execute(select_sql)
    results = cursor.fetchall()

    # 打印查询结果
    for result in results:
        print(result)

    # 关闭游标对象和数据库连接
    cursor.close()
    conn.close()
def student_query_grade_rank(user_id, course_id):
    conn = create_conn()
    if conn is None:
        return
    cursor = conn.cursor()
    # 防止SQL注入
    user_id = conn.escape_string(user_id)
    course_id = conn.escape_string(course_id)

    # 检查操作是否合法
    select_sql = f"SELECT * FROM course WHERE course_id='{course_id}';"
    cursor.execute(select_sql)
    result = cursor.fetchone()
    if not result:
        print("You can only query the grade sheet of the course you teach!")
        return

    # 查询成绩单
    select_sql = f"SELECT * FROM score WHERE course_id='{course_id}' ORDER BY score DESC;"
    cursor.execute(select_sql)
    results = cursor.fetchall()

    # 输出查询结果
    if not results:
        print("No matching record found.")
    else:
        for result in results:
            print(result)
def teacher_query_grade(user_id, course_id=None):
    conn = create_conn()
    if conn is None:
        return
    cursor = conn.cursor()
    # 防止SQL注入
    user_id = conn.escape_string(user_id)
    if course_id is not None:
        course_id = conn.escape_string(course_id)

    # 检查操作是否合法
    select_sql = f"SELECT * FROM course WHERE teacher_id='{user_id}';"
    cursor.execute(select_sql)
    results = cursor.fetchall()
    if not results:
        print("You are not teaching any course!")
        return

    # 查询成绩信息
    if course_id is not None:
        select_sql = f"SELECT * FROM grade WHERE course_id='{course_id}';"
    else:
        select_sql = f"SELECT * FROM grade WHERE teacher_id='{user_id}';"
    cursor.execute(select_sql)
    results = cursor.fetchall()

    # 输出查询结果
    if not results:
        print("No matching record found.")
    else:
        for result in results:
            print(result)
def teacher_update_grade(user_id, course_id, student_id, new_grade):
    conn = create_conn()
    if conn is None:
        return
    cursor = conn.cursor()
    # 防止SQL注入


    # 检查操作是否合法
    select_sql = f"SELECT * FROM score WHERE course_id='{course_id}' AND student_id='{student_id}';"
    cursor.execute(select_sql)
    result = cursor.fetchone()
    if not result:
        print("You can only modify the grade of students in the courses you teach!")
        return

    # 修改成绩信息
    update_sql = f"UPDATE score SET score='{new_grade}' WHERE course_id='{course_id}' AND student_id='{student_id}';"
    cursor.execute(update_sql)
    conn.commit()
    print(f"Updated grade to {new_grade} for student {student_id} in course {course_id} successfully!")
def teacher_query_grade_sheet(user_id, course_id):
    conn = create_conn()
    if conn is None:
        return
    cursor = conn.cursor()
    # 防止SQL注入
    user_id = conn.escape_string(user_id)
    course_id = conn.escape_string(course_id)

    # 检查操作是否合法
    select_sql = f"SELECT * FROM course WHERE teacher_id='{user_id}' AND course_id='{course_id}';"
    cursor.execute(select_sql)
    result = cursor.fetchone()
    if not result:
        print("You can only query the grade sheet of the course you teach!")
        return

    # 查询成绩单
    select_sql = f"SELECT * FROM grade WHERE course_id='{course_id}' ORDER BY grade DESC;"
    cursor.execute(select_sql)
    results = cursor.fetchall()

    # 输出查询结果
    if not results:
        print("No matching record found.")
    else:
        for result in results:
            print(result)
def teacher_query_course(teacher_id):
    conn = create_conn()
    if conn is None:
        return
    cursor = conn.cursor()

    try:
        # 查询课程信息，包括课程ID和名称
        select_sql = f'''
        SELECT course_id, name 
        FROM course 
        WHERE teacher_id='{teacher_id}';
        '''
        cursor.execute(select_sql)
        results = cursor.fetchall()

        # 打印查询结果
        print('您本学期所教授的科目如下： ')
        for result in results:
            print(f"Course ID: {result[0]} | Course Name: {result[1]}")

    except Error as e:
        print(f"Error: {e}")
    # 关闭游标对象和数据库连接
    cursor.close()
    conn.close()
def admin_insert_student(student_id, name, gender, email, phone, password):
    conn = create_conn()
    if conn is None:
        return
    cursor = conn.cursor()

    # 插入学生信息
    insert_sql = f'''
    INSERT INTO student(student_id, name, gender, email, phone, password) 
    VALUES('{student_id}', '{name}', '{gender}', '{email}', '{phone}', '{password}');
    '''
    try:
        cursor.execute(insert_sql)
        conn.commit()
        print(f"Inserted student {name} ({student_id}) successfully!")
    except Exception as e:
        conn.rollback()
        print("Failed to insert student:", e)

    # 关闭游标对象和数据库连接
    cursor.close()
    conn.close()
def admin_insert_teacher(teacher_id, name, gender, email, phone):
    # 防止SQL注入
    conn = create_conn()
    if conn is None:
        return
    cursor = conn.cursor()

    # 插入教师信息
    insert_sql = f"INSERT INTO teacher(teacher_id, name, gender, email, phone) VALUES('{teacher_id}', '{name}', '{gender}', '{email}', '{phone}');"
    try:
        cursor.execute(insert_sql)
        conn.commit()
        print("Insert teacher information successfully!")
    except Exception as e:
        conn.rollback()
        print("Failed to insert teacher information:", e)

    # 关闭游标对象和数据库连接
    cursor.close()
    conn.close()
def admin_insert_course(course_id, course_name, teacher_id):
    conn = create_conn()
    if conn is None:
        return
    cursor = conn.cursor()

    # 插入课程信息
    insert_sql = f"INSERT INTO course(course_id, course_name, teacher_id) VALUES('{course_id}', '{course_name}', '{teacher_id}');"
    try:
        cursor.execute(insert_sql)
        conn.commit()
        print(f"Successfully inserted course: {course_id} - {course_name}")
    except Exception as e:
        print(f"Failed to insert course: {course_id} - {course_name}")
        print(f"Error message: {e}")

    # 关闭游标对象和数据库连接
    cursor.close()
    conn.close()

login(10001,123456,'admin')
# user_id = '201901003'
# user_type = 'student'
# course_id = '10032'
query_student_info('1','admin','201901003')

# select_table('teacher')
# select_table('course')
# teacher_update_grade('1002',course_id,user_id,'95')
# student_query_grade_rank(user_id,course_id)

# query_teacher_info(10012)
# create_tables()
# init_users()
# print_all_tables()
# select_table('teacher')
# select_table('selection')

# student_query_selection(user_id)
# student_select_course(user_id, 10032,select = 'insert')
# # select_table('teacher')
# select_table('score')
# teacher_update_course(1001,10021,1002)
# select_table('course')
# select_table('selection')
# student_query_selection(user_id)
# admin_do_course(10032,'hh','1002',select = 'update',new_course_name='语文') #每门课只能由一个老师教
#
#
# user_id = input("Enter your user ID: ")
# password = input("Enter your password: ")
# user_type = input("Enter your user type (student, teacher, admin): ")
# #示例登录
# login(user_id, password, user_type)
#
# #查询学生信息
# query_student_info(user_id, user_type,target_student_id =201901003)
# update_student_info('00001',user_type,target_student_id='00001',select = 'student_id',newinfo=user_id)
