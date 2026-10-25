
from datetime import datetime, timedelta
import re
import csv

# Sample LinkedIn posts for testing
posts = [
    {
        "role": "Java Developer C2C",
        "location": "Dallas, TX, USA",
        "hours_ago": 3,
        "text": "Hiring Java Developer! Contact recruiter@techjobs.com"
    },
    {
        "role": "Python Developer",
        "location": "Pune, India",
        "hours_ago": 2,
        "text": "Hiring Python developers. Email india@jobs.com"
    },
    {
        "role": "Java Developer C2C",
        "location": "New York, USA",
        "hours_ago": 30,
        "text": "Java opening. Contact oldpost@jobs.com"
    }
]

def extract_email(text):
    emails = re.findall(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        text
    )
    return emails[0] if emails else ""

def filter_posts(posts):
    results = []

    for post in posts:
        is_java = "java developer" in post["role"].lower()
        is_usa = "usa" in post["location"].lower()
        is_recent = post["hours_ago"] <= 24

        if is_java and is_usa and is_recent:
            email = extract_email(post["text"])

            if email:
                results.append({
                    "role": post["role"],
                    "location": post["location"],
                    "email": email,
                    "post_text": post["text"]
                })

    return results

results = filter_posts(posts)

with open("recruiters.csv", "w", newline="", encoding="utf-8") as file:
    fields = ["role", "location", "email", "post_text"]
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(results)

print("\nMatching recruiter posts:")
for result in results:
    print(result)

print(f"\nTotal matching posts: {len(results)}")
print("Results saved to recruiters.csv")


def create_email(role, recruiter_email):
    subject = f"Inquiry Regarding {role} Opportunity"

    body = f"""Hello,

I came across your post regarding a {role} opportunity
and would like to learn more about the position.

Could you please share the job details and requirements?

Thank you for your time.

Best regards,
Your Name
"""

    return subject, body


print("\n========== EMAIL PREVIEW ==========")

for result in results:
    subject, body = create_email(
        result["role"],
        result["email"]
    )

    print("To:", result["email"])
    print("Subject:", subject)
    print(body)
    print("===================================")

    
def remove_duplicates(results):
    unique_results = []
    seen_emails = set()

    for result in results:
        email = result["email"].lower()

        if email not in seen_emails:
            seen_emails.add(email)
            unique_results.append(result)

    return unique_results


unique_results = remove_duplicates(results)

print("\n========== DUPLICATE CHECK ==========")
print("Posts before duplicate check:", len(results))
print("Posts after duplicate check:", len(unique_results))
print("=====================================")


