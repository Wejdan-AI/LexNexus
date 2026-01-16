<template>
  <main class="min-h-screen bg-slate-950 text-slate-100">
    <div class="mx-auto flex max-w-6xl flex-col gap-10 px-6 py-12">
      <header class="space-y-4">
        <p class="text-sm font-semibold uppercase tracking-[0.3em] text-slate-400">
          Operations playbook
        </p>
        <h1 class="text-4xl font-semibold leading-tight text-white sm:text-5xl">
          Operations in Banking (COP)
        </h1>
        <p class="max-w-2xl text-base text-slate-300 sm:text-lg">
          A structured overview of demand intake, branch support, performance
          monitoring, governance, and risk management activities.
        </p>
      </header>

      <section class="grid gap-6 lg:grid-cols-2">
        <article
          v-for="section in sections"
          :key="section.title"
          class="flex h-full flex-col gap-6 rounded-2xl border border-white/10 bg-slate-900/60 p-6 shadow-lg shadow-black/40"
        >
          <div class="flex flex-wrap items-start justify-between gap-4">
            <div>
              <h2 class="text-xl font-semibold text-white">
                {{ section.title }}
              </h2>
              <p v-if="section.tag" class="text-sm text-slate-400">
                {{ section.tag }}
              </p>
            </div>
            <div
              v-if="section.meta"
              class="flex flex-wrap items-center gap-2 text-xs text-slate-300"
            >
              <span
                v-if="section.meta.due"
                class="rounded-full border border-white/10 bg-white/5 px-3 py-1"
              >
                {{ section.meta.due }}
              </span>
              <span
                v-if="section.meta.owner"
                class="rounded-full border border-white/10 bg-white/5 px-3 py-1"
              >
                {{ section.meta.owner }}
              </span>
              <span
                v-if="section.meta.type"
                class="rounded-full border border-white/10 bg-white/5 px-3 py-1"
              >
                {{ section.meta.type }}
              </span>
              <span
                v-if="section.meta.priority"
                class="rounded-full border px-3 py-1 font-semibold"
                :class="priorityClasses[section.meta.priority]"
              >
                {{ section.meta.priority }}
              </span>
            </div>
          </div>

          <div class="space-y-6">
            <div v-for="item in section.items" :key="item.title">
              <h3 class="text-base font-semibold text-slate-100">
                {{ item.title }}
              </h3>
              <ul class="mt-2 list-disc space-y-2 pl-5 text-sm text-slate-300">
                <li v-for="task in item.tasks" :key="task">
                  {{ task }}
                </li>
              </ul>
            </div>
          </div>
        </article>
      </section>
    </div>
  </main>
</template>

<script setup>
const priorityClasses = {
  P1: 'border-rose-400/50 bg-rose-500/20 text-rose-100',
  P2: 'border-amber-300/50 bg-amber-500/20 text-amber-100',
  P3: 'border-emerald-300/40 bg-emerald-500/20 text-emerald-100',
}

const sections = [
  {
    title: 'Demand Management',
    tag: '#demand_management',
    meta: {
      due: 'Jan 17, 2026, 6:00 AM',
      owner: 'lexlink',
      type: 'Bullet',
      priority: 'P1',
    },
    items: [
      {
        title: 'Request Intake and Classification',
        tasks: [
          'Log requests into the system.',
          'Classify requests using the approved categorization (Access to systems, Cash, Equipment, Forms, Accounts, Policy, Others).',
        ],
      },
      {
        title: 'Priority Setting and SLA',
        tasks: [
          'Assign priority from P1 to P4 based on impact/urgency matrix.',
          'Inform requester of available service level (SLA).',
        ],
      },
      {
        title: 'Execution and Follow-Up',
        tasks: [
          'Assign responsible personnel and document steps.',
          'Track progress according to SLA.',
        ],
      },
      {
        title: 'Cash Over Limit Approval',
        tasks: [
          'Daily review and approval of cash over limit requests via email and e-register; track and manage.',
        ],
      },
    ],
  },
  {
    title: 'Branch Visits and Support',
    tag: '#branch_support',
    meta: {
      due: 'Jan 18, 2026, 6:00 AM',
      owner: 'lexlink',
      type: 'Bullet',
      priority: 'P2',
    },
    items: [
      {
        title: 'Branch Visits',
        tasks: [
          'Prepare annual visit plan including routine and audit visits.',
          'Conduct visits with comprehensive coverage.',
        ],
      },
      {
        title: 'Monitoring and Closing Observations',
        tasks: [
          'Correct observations within 5 business days.',
          'Verify evidence and perform final closure.',
        ],
      },
      {
        title: 'Surprise Checks',
        tasks: ['Conduct unannounced verifications monthly.'],
      },
    ],
  },
  {
    title: 'Performance and Claims Management',
    tag: '#performance_management',
    meta: {
      due: 'Jan 17, 2026, 6:00 AM',
      owner: 'lexlink',
      type: 'Bullet',
      priority: 'P3',
    },
    items: [
      {
        title: 'Daily Monitoring of Self-Service Machines',
        tasks: ['Review electronic journals.', 'Escalate issues and propose improvements.'],
      },
      {
        title: 'Claims and Exceptions Management',
        tasks: [
          'Follow up claims with branches during and after work hours.',
          'Monitor ATM availability and performance.',
        ],
      },
      {
        title: 'Discrepancy Management & Monitoring',
        tasks: [
          'Monitor and reduce discrepancies; create material for highest products; quarterly reporting.',
        ],
      },
    ],
  },
  {
    title: 'Management Meetings and Updates',
    tag: '#management_meetings',
    items: [
      {
        title: 'Weekly Updates',
        tasks: [
          'Prepare variance files and weekly updates.',
          'Present service reports and executive council updates.',
        ],
      },
      {
        title: 'Performance Indicators',
        tasks: [
          'Gather data from branches and share information with regions.',
          'Update dashboards and monitor accuracy.',
        ],
      },
      {
        title: 'Quarterly Meetings',
        tasks: [
          'Prepare DMG materials based on latest updates and area needs; deliver quarterly meetings.',
        ],
      },
    ],
  },
  {
    title: 'Governance and Compliance',
    tag: '#governance',
    meta: {
      due: 'Jan 19, 2026, 6:00 AM',
      owner: 'lexlink',
      type: 'Checkbox',
      priority: 'P2',
    },
    items: [
      {
        title: 'Awareness and Knowledge Sessions',
        tasks: [
          'Draft and send materials to branches.',
          'Deliver sessions during visits and quarterly meetings.',
        ],
      },
      {
        title: 'Saudi Central Bank (SAMA) Reports',
        tasks: [
          'Update all monthly/quarterly reports related to branches.',
          'Review, ensure accuracy, and submit on time.',
        ],
      },
      {
        title: 'Audit Cooperation & Evidence Preparation',
        tasks: [
          'Prepare branches before audit visits; coordinate responses; provide evidence; implement recommendations.',
        ],
      },
    ],
  },
  {
    title: 'Risk Management',
    tag: '#risk_management',
    meta: {
      due: 'Jan 18, 2026, 6:00 AM',
      owner: 'lexlink',
      type: 'Bullet',
      priority: 'P3',
    },
    items: [
      {
        title: 'Operational Risk Trends Report',
        tasks: ['Report quarterly to Senior Management on operational risk trends.'],
      },
      {
        title: 'Risk Appetite Monitoring',
        tasks: ['Monitor adherence to risk appetite and tolerance levels.'],
      },
      {
        title: 'Incident Management',
        tasks: [
          'Document incidents and perform root cause analysis.',
          'Implement continuous improvement initiatives.',
        ],
      },
    ],
  },
]
</script>
