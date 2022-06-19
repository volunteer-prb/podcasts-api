export interface StorageInterface {
  length(): number;
  clear(): void;
  getItem<T>(key: string): T | null;
  removeItem(key: string): void;
  setItem<T>(key: string, value: T): void;
}

export abstract class BaseStorage implements StorageInterface {
  constructor(private storage: Storage) {}

  length(): number {
    return this.storage.length;
  }

  clear() {
    this.storage.clear();
  }

  getItem<T>(key: string): T | null {
    try {
      return JSON.parse(this.storage.getItem(key) as string);
    } catch {
      return null;
    }
  }

  removeItem(key: string) {
    this.storage.removeItem(key);
  }

  setItem<T>(key: string, value: T) {
    this.storage.setItem(key, JSON.stringify(value));
  }
}
