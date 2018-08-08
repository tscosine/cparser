
	pid_t pid;
	const struct auditd_connection *ac;

	rcu_read_lock();
	ac = rcu_dereference(auditd_conn);
	if (!ac || !ac->pid)
		pid = 0;
	else
		pid = pid_vnr(ac->pid);
	rcu_read_unlock();

	return pid;