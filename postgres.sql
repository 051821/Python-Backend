SELECT * FROM posts LEFT JOIN writer ON posts.user_id = writer.id


select writer.id,Count(*) from posts LEFT JOIN writer on posts.user_id = writer.id  group by writer.id
select writer.id,Count(*) from posts RIGHT JOIN writer on posts.user_id = writer.id  group by writer.id
select * from posts RIGHT JOIN writer on posts.user_id = writer.id 

SELECT writer.id, COUNT(posts.id) AS user_post_count FROM posts JOIN writer ON posts.user_id = writer.id GROUP BY writer.id;

SELECT posts.id, COUNT(votes.post_id) AS vote_count
FROM posts
LEFT JOIN votes ON posts.id = votes.post_id
GROUP BY posts.id;

select * from votes
select * from writer
select * from posts