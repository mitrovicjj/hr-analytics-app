def get_education_counts():
    return '''
    SELECT education_level, COUNT(*) AS num_candidates
    FROM candidates
    GROUP BY education_level
    ORDER BY num_candidates DESC;
    '''


def get_avg_experience_by_gender():
    return '''
    SELECT gender, AVG(experience) AS avg_experience
    FROM candidates
    GROUP BY gender;
    '''


def get_company_type_counts():
    return '''
    SELECT company_type, COUNT(*) AS count
    FROM candidates
    GROUP BY company_type
    ORDER BY count DESC;
    '''


def get_last_new_job_counts():
    return '''
    SELECT last_new_job, COUNT(*) AS count
    FROM candidates
    GROUP BY last_new_job
    ORDER BY count DESC;
    '''


def get_top_cities(limit=10):
    return f'''
    SELECT city, COUNT(*) AS count
    FROM candidates
    GROUP BY city
    ORDER BY count DESC
    LIMIT {limit};
    '''


def get_avg_training_by_city_edu():
    return '''
    SELECT
        city,
        education_level,
        ROUND(AVG(training_hours), 2) AS avg_training_hours
    FROM candidates
    GROUP BY city, education_level
    ORDER BY avg_training_hours DESC;
    '''


def get_change_ratio_by_experience():
    return '''
    SELECT
        experience,
        COUNT(*) AS total_people,
        SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) AS changed_jobs,
        ROUND(SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 2) AS change_ratio
    FROM candidates
    GROUP BY experience
    ORDER BY experience;
    '''

def get_masters_phd_change_ratio():
    return '''
    SELECT
        education_level,
        COUNT(*) AS total_candidates,
        SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) AS changed_jobs,
        ROUND(SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 2) AS change_ratio
    FROM candidates
    WHERE education_level IN ('Masters', 'Phd')
    GROUP BY education_level
    ORDER BY education_level;
    '''

def get_change_ratio_by_company_type():
    return '''
    SELECT
        company_type,
        COUNT(*) AS total_candidates,
        SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) AS changed_jobs,
        ROUND(SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 2) AS change_ratio
    FROM candidates
    GROUP BY company_type
    ORDER BY change_ratio DESC;
    '''