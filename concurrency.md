# Lost Update

```mermaid
sequenceDiagram
     participant T1
    participant Database
    participant T2
    Note over T1, T2: Alice hasnt entered into a raffle yet and has 100 points, enough for one raffle ticket
    T1->>Database: check how many points before entering raffle 3
    T1->>Database: "SELECT COALESCE(SUM(point_change),0) FROM point_ledger WHERE user_id = :user_id)"
    T1->>Database: check Alice has enough points to continue
    T2->>Database: Alice wants to enter into raffle 4 as well
    T2->>Database: "SELECT COALESCE(SUM(point_change),0) FROM point_ledger WHERE user_id = :user_id)"
    T2->>Database: check Alice has enough points to continue
    T2->>Database: "INSERT INTO raffle_entries (raffle_id,user_id) VALUES(:raffle_id,:user_id)"
    T2->>Database: "INSERT INTO point_ledger (user_id,point_change) VALUES (:user_id,:point_change)"
    Note over T1, T2: Alice is now entered into raffle 4 and has 0 points
    T1->>Database: "INSERT INTO raffle_entries (raffle_id,user_id) VALUES(:raffle_id,:user_id)"
    T1->>Database: "INSERT INTO point_ledger (user_id,point_change) VALUES (:user_id,:point_change)"
    Note over T1, T2: Alice's Point Balance is 100 - 100 = 0. We lost the previous update where she already used her 100 points.
```
This diagram shows how T1 read a data item and then T2 updates the data item, then T1 (based on its earlier read value) updates the data item and commits. to ensure that this doesnt happen, we use Atomic Operations that encompass all the steps needed to update the data so there is no way for this phenomena to happen. This works because it makes sure that either all operations go through, or none.

# Dirty Read

```mermaid
sequenceDiagram
    participant T1
    participant Database
    participant T2
    Note over T1, T2: Bob has 99 points and is gonna write a review
    T1->>Database: write a review on a pair of shoes
    T1->>Database: INSERT INTO point_ledger (user_id,point_change) 
    T2->>Database: Bob wants to enter into raffle 3 as well
    T2->>Database: cur_points = conn.execute(sqlalchemy.text("SELECT COALESCE(SUM(point_change),0) FROM point_ledger WHERE user_id = :user_id)");
    T2->>Database: check Bob has enough points to continue
    T2->>Database: conn.execute(sqlalchemy.text("INSERT INTO raffle_entries (raffle_id,user_id) VALUES(:raffle_id,:user_id)");
    T2->>Database: conn.execute(sqlalchemy.text("INSERT INTO point_ledger (user_id,point_change) VALUES (:user_id,:point_change)");
    Note over T1, T2: Bob is now entered into raffle 3 and has 0 points
    T1->>Database: Transaction cancelled due to invalid rating
    Note over T1, T2: Bob now is in raffle 3 but he he never reach the 100 points need for it
```

This diagram shows how T1 wrote data uncommitted and then T2 read that uncommitted data and did stuff with it. But T1 then fails and the uncommitted data was read but it actually never should have existed. To prevent this we use Transactions and keep them Atomic so that if one part of the transaction fails none of it gets written. This solves it because it ensures isolation between each call.

# Non Repeatable read

```mermaid
sequenceDiagram
     participant T1
    participant Database
    participant T2
    Note over T1, T2: Kameron hasnt entered into a raffle yet and has 100 points, enough for one raffle ticket
    T1->>Database: check how many points before entering raffle 3
    T1->>Database: cur_points = "SELECT COALESCE(SUM(point_change),0) FROM point_ledger WHERE user_id = :user_id)"
    T1->>Database: check Kameron has enough points to continue
    T2->>Database: Kameron wants to enter into raffle 4 as well
    T2->>Database: cur_points = "SELECT COALESCE(SUM(point_change),0) FROM point_ledger WHERE user_id = :user_id)"
    T2->>Database: check Kameron has enough points to continue
    T2->>Database: "INSERT INTO raffle_entries (raffle_id,user_id) VALUES(:raffle_id,:user_id)"
    T2->>Database: "INSERT INTO point_ledger (user_id,point_change) VALUES (:user_id,:point_change)"
    Note over T1, T2: Kameron is now entered into raffle 4 and has 0 points
    T1->>Database: "INSERT INTO raffle_entries (raffle_id,user_id) VALUES(:raffle_id,:user_id)"
    T1->>Database: "SELECT COALESCE(SUM(point_change),0) FROM point_ledger WHERE user_id = :user_id)"
    T1->>Database: "INSERT INTO point_ledger (user_id,point_change) VALUES (:user_id,:point_change)"
    Note over T1, T2: Kameron's Point Balance is 100 - 0 = -100. We read data and when we went to read it again it had changed, causing a discrepincy in our data.
```

This diagram shows how T1 read the same row twice and gots a different value each time. We solved this issue by keeping all our commands in the same transaction. This solves it because it ensures isolation between each call.


