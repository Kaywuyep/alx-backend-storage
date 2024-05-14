#!/usr/bin/env python3
"""
Improve 12-log_stats.py by adding the top 10 of the most present IPs in the collection nginx of the database logs:
"""

from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    """Prints stats about Nginx request logs"""
    # Total number of logs
    total_logs = nginx_collection.count_documents({})
    print('{} logs'.format(total_logs))

    # Methods statistics
    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        method_count = nginx_collection.count_documents({'method': method})
        print('\tmethod {}: {}'.format(method, method_count))

    # Number of GET requests to /status
    status_check_count = nginx_collection.count_documents({'method': 'GET', 'path': '/status'})
    print('{} status check'.format(status_check_count))

    # Top 10 IP addresses
    print('IPs:')
    pipeline = [
        {'$group': {'_id': '$ip', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 10}
    ]
    top_ips = nginx_collection.aggregate(pipeline)
    for ip in top_ips:
        print('\t{}: {}'.format(ip['_id'], ip['count']))


def run_db():
    ""Provides some stats about Nginx logs stored in MongoDB."""
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    print_nginx_request_logs(nginx_collection)


if __name__ == '__main__':
    run_db()
