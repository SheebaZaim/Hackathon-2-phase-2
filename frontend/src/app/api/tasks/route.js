import { NextResponse } from 'next/server';

// Mock data store for tasks
let tasks = [
  { id: 1, title: 'Learn React', description: 'Study React fundamentals', completed: true, status: 'completed', priority: 'medium', created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
  { id: 2, title: 'Build Todo App', description: 'Create a full-featured todo application', completed: false, status: 'in-progress', priority: 'high', created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
];

let nextId = 3;

export async function GET(request) {
  try {
    // Simulate delay for realistic API feel
    await new Promise(resolve => setTimeout(resolve, 200));

    return NextResponse.json(tasks);
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch tasks' }, { status: 500 });
  }
}

export async function POST(request) {
  try {
    const data = await request.json();

    const newTask = {
      id: nextId++,
      title: data.title,
      description: data.description || '',
      completed: false,
      status: data.status || 'pending',
      priority: data.priority || 'medium',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };

    tasks.push(newTask);

    return NextResponse.json(newTask, { status: 201 });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to create task' }, { status: 500 });
  }
}

export async function PUT(request, { params }) {
  try {
    const { id } = params;
    const taskId = parseInt(id);
    const data = await request.json();

    const taskIndex = tasks.findIndex(task => task.id === taskId);
    if (taskIndex === -1) {
      return NextResponse.json({ error: 'Task not found' }, { status: 404 });
    }

    tasks[taskIndex] = {
      ...tasks[taskIndex],
      ...data,
      id: taskId,
      updated_at: new Date().toISOString()
    };

    return NextResponse.json(tasks[taskIndex]);
  } catch (error) {
    return NextResponse.json({ error: 'Failed to update task' }, { status: 500 });
  }
}

export async function DELETE(request, { params }) {
  try {
    const { id } = params;
    const taskId = parseInt(id);

    const taskIndex = tasks.findIndex(task => task.id === taskId);
    if (taskIndex === -1) {
      return NextResponse.json({ error: 'Task not found' }, { status: 404 });
    }

    tasks.splice(taskIndex, 1);

    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to delete task' }, { status: 500 });
  }
}

// Helper to get dynamic route parameters
export function generateStaticParams() {
  return tasks.map(task => ({
    id: task.id.toString()
  }));
}